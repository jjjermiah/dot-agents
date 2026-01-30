#!/usr/bin/env -S pixi exec --spec python=3.12 -- python
"""
Skill Token Estimator - Extracts frontmatter and estimates token count from SKILL.md

Usage:
    estimate_tokens.py <path/to/SKILL.md>
    estimate_tokens.py <path/to/skill-folder>

Examples:
    estimate_tokens.py skills/public/my-skill/SKILL.md
    estimate_tokens.py skills/public/my-skill

Output: XML format with the following structure:
    <skill-analysis>
      <skill-name>...</skill-name>
      <skill-path>...</skill-path>
      <frontmatter>
        <description-length>...</description-length>
        <description-tokens>...</description-tokens>
      </frontmatter>
      <body>
        <lines>...</lines>
        <characters>...</characters>
        <tokens>...</tokens>
      </body>
      <references count="N">
        <total-tokens>...</total-tokens>
        <reference file="...">
          <lines>...</lines>
          <tokens>...</tokens>
        </reference>
      </references>
      <totals>
        <lines>...</lines>
        <tokens>...</tokens>
      </totals>
      <recommendations>
        <recommendation>...</recommendation>
      </recommendations>
      <efficiency-rating category="compact|efficient|moderate|large">...</efficiency-rating>
    </skill-analysis>
"""

import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def estimate_tokens(text):
    """
    Estimate token count from text.

    Uses a simple heuristic: ~4 characters per token for English text.
    This is a rough estimate - actual tokenization varies by model.

    Args:
        text: String to estimate

    Returns:
        Estimated token count (int)
    """
    if not text:
        return 0
    # Rough estimate: 4 chars per token for code/English mix
    return len(text) // 4


def extract_frontmatter(content):
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Full markdown content

    Returns:
        Tuple of (frontmatter_text, body_text) or (None, content) if no frontmatter
    """
    if not content.startswith("---"):
        return None, content

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, content

    frontmatter = match.group(1)
    body = content[match.end() :].strip()

    return frontmatter, body


def parse_frontmatter_fields(frontmatter_text):
    """
    Parse key fields from frontmatter text.

    Args:
        frontmatter_text: YAML frontmatter content

    Returns:
        Dict with field names and values
    """
    fields = {}

    # Extract name
    name_match = re.search(r"^name:\s*(.+)$", frontmatter_text, re.MULTILINE)
    if name_match:
        fields["name"] = name_match.group(1).strip()

    # Extract description (handle multi-line)
    desc_match = re.search(
        r"^description:\s*[>|]?(.*?)(?=^\w+:|\Z)",
        frontmatter_text,
        re.MULTILINE | re.DOTALL,
    )
    if desc_match:
        desc = desc_match.group(1).strip()
        # Clean up multi-line descriptions
        desc = re.sub(r"\n\s+", " ", desc)
        fields["description"] = desc
        fields["description_length"] = len(desc)
        fields["description_tokens"] = estimate_tokens(desc)

    return fields


def analyze_skill(skill_path):
    """
    Analyze a skill and estimate token counts.

    Args:
        skill_path: Path to skill folder or SKILL.md file

    Returns:
        Dict with analysis results
    """
    skill_path = Path(skill_path)

    # Handle both folder and file paths
    if skill_path.is_dir():
        skill_md = skill_path / "SKILL.md"
        skill_folder = skill_path
    else:
        skill_md = skill_path
        skill_folder = skill_path.parent

    if not skill_md.exists():
        return {"error": f"SKILL.md not found: {skill_md}"}

    # Read SKILL.md
    content = skill_md.read_text()

    # Extract frontmatter and body
    frontmatter, body = extract_frontmatter(content)

    if frontmatter is None:
        return {"error": "No YAML frontmatter found in SKILL.md"}

    # Parse frontmatter
    fields = parse_frontmatter_fields(frontmatter)

    # Analyze body
    body_lines = body.split("\n")
    body_chars = len(body)
    body_tokens = estimate_tokens(body)

    # Analyze references
    references_dir = skill_folder / "references"
    ref_analysis = []
    total_ref_tokens = 0

    if references_dir.exists():
        for ref_file in sorted(references_dir.glob("*.md")):
            ref_content = ref_file.read_text()
            ref_tokens = estimate_tokens(ref_content)
            ref_analysis.append(
                {
                    "file": ref_file.name,
                    "lines": len(ref_content.split("\n")),
                    "tokens": ref_tokens,
                }
            )
            total_ref_tokens += ref_tokens

    # Calculate totals
    total_tokens = fields.get("description_tokens", 0) + body_tokens + total_ref_tokens

    return {
        "skill_name": fields.get("name", "unknown"),
        "skill_path": str(skill_md),
        "frontmatter": {
            "description_length": fields.get("description_length", 0),
            "description_tokens": fields.get("description_tokens", 0),
        },
        "body": {
            "lines": len(body_lines),
            "characters": body_chars,
            "tokens": body_tokens,
        },
        "references": {
            "count": len(ref_analysis),
            "files": ref_analysis,
            "total_tokens": total_ref_tokens,
        },
        "totals": {
            "tokens": total_tokens,
            "lines": len(body_lines) + sum(r["lines"] for r in ref_analysis),
        },
        "recommendations": generate_recommendations(
            len(body_lines), body_tokens, len(ref_analysis), total_ref_tokens
        ),
    }


def generate_recommendations(body_lines, body_tokens, ref_count, ref_tokens):
    """Generate recommendations based on token analysis."""
    recommendations = []

    # Check body length
    if body_lines > 500:
        recommendations.append(
            f"⚠️  Body is {body_lines} lines (recommended: <500). Consider splitting to references."
        )

    # Check if references would help
    if body_tokens > 2000 and ref_count == 0:
        recommendations.append(
            f"💡 Body is ~{body_tokens} tokens. Consider creating references/ for detailed content."
        )

    # Check reference distribution
    if ref_count > 0:
        avg_ref_tokens = ref_tokens // ref_count if ref_count > 0 else 0
        if avg_ref_tokens > 1500:
            recommendations.append(
                f"💡 References average ~{avg_ref_tokens} tokens each. Consider splitting large references."
            )

    # Token efficiency check
    total_content_tokens = body_tokens + ref_tokens
    if total_content_tokens > 4000:
        recommendations.append(
            f"📊 Total content is ~{total_content_tokens} tokens. Ensure progressive disclosure is effective."
        )

    return recommendations


def output_xml(results):
    """Output results as XML."""
    if "error" in results:
        root = Element("error")
        root.text = results["error"]
        print(tostring(root, encoding="unicode"))
        return

    root = Element("skill-analysis")

    # Skill info
    SubElement(root, "skill-name").text = results["skill_name"]
    SubElement(root, "skill-path").text = results["skill_path"]

    # Frontmatter
    fm_elem = SubElement(root, "frontmatter")
    SubElement(fm_elem, "description-length").text = str(
        results["frontmatter"]["description_length"]
    )
    SubElement(fm_elem, "description-tokens").text = str(
        results["frontmatter"]["description_tokens"]
    )

    # Body
    body_elem = SubElement(root, "body")
    SubElement(body_elem, "lines").text = str(results["body"]["lines"])
    SubElement(body_elem, "characters").text = str(results["body"]["characters"])
    SubElement(body_elem, "tokens").text = str(results["body"]["tokens"])

    # References
    refs_elem = SubElement(root, "references")
    refs_elem.set("count", str(results["references"]["count"]))
    SubElement(refs_elem, "total-tokens").text = str(
        results["references"]["total_tokens"]
    )

    for ref in results["references"]["files"]:
        ref_elem = SubElement(refs_elem, "reference")
        ref_elem.set("file", ref["file"])
        SubElement(ref_elem, "lines").text = str(ref["lines"])
        SubElement(ref_elem, "tokens").text = str(ref["tokens"])

    # Totals
    totals_elem = SubElement(root, "totals")
    SubElement(totals_elem, "lines").text = str(results["totals"]["lines"])
    SubElement(totals_elem, "tokens").text = str(results["totals"]["tokens"])

    # Recommendations
    recs_elem = SubElement(root, "recommendations")
    for rec in results["recommendations"]:
        rec_elem = SubElement(recs_elem, "recommendation")
        rec_elem.text = rec

    # Rating
    total = results["totals"]["tokens"]
    if total < 1000:
        rating = "compact"
    elif total < 2500:
        rating = "efficient"
    elif total < 4000:
        rating = "moderate"
    else:
        rating = "large"

    rating_elem = SubElement(root, "efficiency-rating")
    rating_elem.set("category", rating)
    rating_elem.text = str(total)

    # Output pretty-printed XML
    xml_str = tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    # Remove extra blank lines that minidom adds
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    print("\n".join(lines))


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    skill_path = sys.argv[1]
    results = analyze_skill(skill_path)
    output_xml(results)

    # Exit with error code if there was an error
    if "error" in results:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
