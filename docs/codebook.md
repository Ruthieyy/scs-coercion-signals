# Codebook: coercion signals in official PRC statements (v1, 2026-10-19)

**Unit:** one sentence spoken by the PRC MFA spokesperson in a regular press conference, in an answer to a question about the **Taiwan / South China Sea / Philippines / maritime-dispute** topic set (EN or ZH).

**Label set:** exactly one of `action`, `threat` or `neither`.

## ACTION
The sentence **reports, confirms, announces or justifies a specific coercive measure that the PRC (MFA, PLA, CCG or another state organ) has taken or is currently taking** against another party in the topic set.
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
- `silver`: produced by a keyword/regex labeler (`src/label_rules.py`) that implements this codebook. These are noisy and are used only as weak training data.
- `agent`: labeled one by one by the AI research assistant (Grok Bot), reading each sentence against this codebook. **These are not human labels.** They are the validation and test set for now, and are exported for human review in `data/labels/for_human_review.csv`.
- `human`: reserved for labels confirmed or corrected by Yutong. Until then, every reported metric is **agreement with agent labels**.

## Decision rules added while labeling (v1.1)
5. Fatalistic predictions with no PRC-imposed cost ("doomed to fail", "a dead end", "will get nowhere", "自取灭亡") → **neither**.
6. Declarations of resolve with no warning to an addressee ("China will not waver", "nothing will deter China") → **neither**. Warnings to an addressee ("no one should underestimate…") → **threat**.
7. Urging others to "stop playing with fire", or calling another party's move "playing with fire" → **neither**. "Those who play with fire will perish" → **threat**.
8. Recounting *past* warnings ("we warned that all consequences would be borne by the US") → **neither**.
9. The formula "the Taiwan question is … the first red line that must not be crossed" → **threat** (rule: red line). It is extremely frequent, so threat counts are dominated by boilerplate. The series should be read as *intensity of red-line rhetoric*, not as novel threats.
