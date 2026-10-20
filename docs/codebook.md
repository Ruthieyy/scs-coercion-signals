# Codebook: coercion signals in official PRC statements (v1.2, 2026-10-20; v1 2026-10-19)

**Unit:** one sentence spoken by the PRC MFA spokesperson in a regular press conference, in an answer to a question about the **Taiwan / South China Sea / Philippines / maritime-dispute** topic set (EN or ZH).

**Label set:** exactly one of `action`, `threat` or `neither`.

## ACTION
The sentence **reports, confirms or announces a specific coercive measure that the PRC (MFA, PLA, CCG or another state organ) has taken or is currently taking** against another party in the topic set. Since v1.2, justifying or restating the legitimacy of a measure already taken is *not* action (rule 10).
- Examples: drills or "joint combat readiness patrols"; CCG "took necessary control measures", water cannon, expelling, boarding or interception; sanctions or countermeasures imposed on named entities or people; baselines declared; patrols "organised in accordance with law".
- Diplomatic démarches **count only if they are a measure, not a statement**. "Has lodged stern representations" is *not* action. It is routine protest and is coded `neither`, because it is ubiquitous and imposes no cost.
- Examples: "The China Coast Guard took necessary measures in accordance with the law to stop the Philippine vessels." / "China has decided to impose sanctions on …" / "中国海警依法采取管控措施" / "解放军东部战区组织联合演习".

## THREAT
The sentence **warns of future or conditional costs, force or consequences**, or draws a red line, *without* reporting an executed measure.
- Examples: "will take resolute and forceful measures", "bear all the consequences", "those who play with fire will get burned", "do not underestimate…", "will not sit idly by", "any provocation will be met with…", "China will take all necessary measures", "the PLA stands ready"; demands to "stop provocations immediately" when paired with a consequence.
- Examples: "任何武装台湾的行径都将面临严重后果" / "中方将采取一切必要措施" / "玩火者必自焚" / "不要低估…坚定意志".

## NEITHER
Everything else:
- statements of position or history ("Taiwan is part of China", "the arbitral award is null and void");
- general criticism of others without a threat ("the US move seriously undermines peace");
- calls for dialogue;
- routine protest ("lodged stern representations", "strongly deplore");
- denial, procedure, and "refer to competent authorities".

## Decision rules
1. If a sentence contains both an executed measure and a warning, code **action**. Executed measures are rarer and more informative.
2. "Firmly oppose", "strongly dissatisfied" and "urge X to stop…" with no consequence clause are **neither**.
3. Generic "safeguard sovereignty" is **neither**. "Will take all necessary measures to safeguard sovereignty" is **threat** (conditional force).
4. Hypothetical or historical measures ("in 2016 China…") are **neither** unless they are restated as ongoing.

## Label provenance (be honest)
- `silver`: produced by a keyword/regex labeler (`src/label_rules.py`). Noisy; used only as weak training data.
- `agent`: labeled one by one by the AI research assistant (Grok Bot) against this codebook. Not human labels. Column `agent_label` in `data/labels/agent_labeled.csv` keeps the original v1.1 label.
- `ai2`: labels from a **second, independent AI model** provided by the author, for the 190 held-out sentences (`ai2_label`, `ai2_note` in `data/labels/for_human_review.csv`; `src/merge_ai2_labels.py`). Not human labels. AI–AI agreement with `agent`: κ = 0.935 (184/190). The 6 disagreements were resolved per rules 5 and 8 using the ai2 label (pre-revision gold kept in `label_v1_1`).
- `human`: **hand labels by the author, no AI**, for a stratified random 40-sentence subset of the held-out set (`data/labels/human_spotcheck_40.csv`: `initial_human`, `final_human`, `adjudicated`, `borderline`; copied to `human_label` in `for_human_review.csv` and `agent_labeled.csv`). Initial human vs. AI agreement was 26/40, κ = 0.457. The author adjudicated the 14 disagreements (7 to the AI label, 6 kept, 1 third label, flagged borderline), which led to v1.2 below. The adjudication worksheet is `data/labels/adjudication_14.csv`; its 最终标签 column is a draft, and the final labels the author confirmed are in `FINAL` in `src/apply_codebook_v12.py`.
- `agent_v1.2`: the assistant re-applied the v1.2 rules to all sentences; 22 changed (16 action → neither under rule 10, 5 neither → threat under revised rule 5, 1 threat → neither). Each change and its reason is in `agent_v12_label` / `v12_reason` (`src/apply_codebook_v12.py`). These relabels were made after seeing the adjudicated human labels.
- Final `label` = human where available, else the v1.2 AI label. Website boilerplate scraped from mfa.gov.cn (exit-site popup "您即将离开外交部门户网站…", copyright/ICP footer) is not speech; it is removed by `segment_mfa.is_junk` (288 rows) and excluded from training and evaluation.

## Decision rules added while labeling (v1.1)
5. ~~Fatalistic predictions with no PRC-imposed cost → **neither**.~~ *Superseded by revised rule 5 in v1.2 below.*
6. Declarations of resolve with no warning to an addressee ("China will not waver", "nothing will deter China") → **neither**. Warnings to an addressee ("no one should underestimate…") → **threat**.
7. Urging others to "stop playing with fire", or calling another party's move "playing with fire" → **neither**. "Those who play with fire will perish" → **threat**.
8. Recounting *past* warnings ("we warned that all consequences would be borne by the US") → **neither**.
9. The formula "the Taiwan question is … the first red line that must not be crossed" → **threat** (rule: red line). It is extremely frequent, so threat counts are dominated by boilerplate. The series should be read as *intensity of red-line rhetoric*, not as novel threats.

## Codebook v1.2 (2026-10-20): revisions decided by the author after the human spot-check
These were decided by the author (Yutong Yao) after hand-labeling 40 sentences and adjudicating the 14 disagreements with the AI labels.

**5 (revised). Threat requires all three:** (i) an explicit addressee (正告 / 警告 / "beware", "make clear to" a named party), (ii) a targeted behaviour of that party, and (iii) an adverse outcome for them. When all three are present the sentence is **threat**, even if the outcome is phrased fatalistically ("死路一条", "doomed to fail").
- Threat: "我们要正告台湾当局，'台独'是死路一条…注定会以失败告终。" / "The Taiwan authorities should also beware that any attempt to seek independence by colluding with external forces is doomed to fail."
- Neither: arguments from historical fact or trend that a goal must fail, with no addressed warning ("任何逆历史潮流的图谋注定失败", "…只会自取灭亡", "'Taiwan independence' is a dead end").
- The word 正告 / warn alone does not automatically make a sentence threat; the content must meet (i)–(iii).
- Rules 6, 7 and 9 (warnings not to underestimate, "those who play with fire will perish", the red-line formula) are unchanged.

**10 (new). Action only when the statement announces or informs** that a specific measure has been or is being taken ("China Coast Guard took necessary measures", "外交部网站公布的…制裁的决定", "China has decided to take countermeasures against…").
- Statements that restate a stance about a measure already taken, or justify / explain its purpose or legitimacy, are **neither** (stance): "我们已经清楚地阐明，中方…进行军事演训是正当、合理、合法的", "中方开展联合演训，是对…的坚决惩戒", "the measure taken is part of our legitimate countermeasures".
- If a sentence both reports a measure and adds a legitimacy clause ("CCG took necessary measures…, which were lawful and restrained"), it is **action** (the reporting part decides). If the reporting is subordinate to a justification ("With the aim of defending national security…, China took measures…, which is fully legitimate"), it is **neither** (author's adjudication of en001298).

