def summarize_meeting(motions, seconds, decisions, actions):
    

    summary_lines = []

    # Motion statistics
    summary_lines.append(f"{len(motions)} motion(s) were proposed.")

    # Second statistics
    summary_lines.append(f"{len(seconds)} motion(s) were seconded.")

    # Decision statistics
    summary_lines.append(f"{len(decisions)} decision(s) were made.")

    # Action item statistics
    summary_lines.append(f"{len(actions)} action item(s) were identified.")

    # Additional interpretation
    if decisions:
        summary_lines.append("\nKey Outcomes:")
        for d in decisions:
            summary_lines.append(f"- {d}")

    if actions:
        summary_lines.append("\nAssigned Actions:")
        for a in actions:
            summary_lines.append(f"- {a}")

    return "\n".join(summary_lines)