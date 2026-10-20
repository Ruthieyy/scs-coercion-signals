"""Silver labeler implementing docs/codebook.md with keyword/regex rules (EN + ZH). Noisy by design."""
import re
ACTION = {"en": r"(took|taken|takes|has taken) (necessary|resolute|forceful)? ?(control )?measures (in accordance with|against|to)|control measures|expelled|drove (it|them) away|warned (it|them) off|boarded|water cannon|(decided|decides|has decided) to (impose|sanction|take countermeasures)|imposes? (sanctions|countermeasures)|sanctions? on|countermeasures against|(conducted|conducting|organized|organised|holding|held) (joint |military |combat-readiness |law enforcement )?(drills|exercises|patrols?)|joint combat readiness patrol|announced the baselines|baselines of the territorial sea|law enforcement (patrol|inspection)s? (were|was|has been)",
          "zh": r"(依法|已)?采取(了)?(必要|坚决|有力)?(的)?管控措施|采取(了)?管控|驱离|登临|登检|水炮|决定(对|对其)?.{0,20}(采取反制|实施制裁|反制措施)|(采取|实施)(了)?反制措施|制裁|(组织|开展|进行|举行)(了)?.{0,12}(演习|演训|巡航|巡逻|战备警巡|执法巡查)|公布.{0,10}领海基线"}
THREAT = {"en": r"will (take|adopt) (all )?(necessary|resolute|forceful|firm|strong)(,? (and|&) (forceful|strong|resolute))? (measures|steps|countermeasures)|bear (all )?the consequences|consequences|play(ing|s)? with fire|get burned|(do not|never|no one should) underestimate|will not sit idly|will not (tolerate|allow)|will be (met|crushed|smashed)|doomed to fail|dead end|red line|stands? ready|at all costs|leave no room|will (respond|hit back|fight back)|(firm|strong) response",
          "zh": r"将(采取|坚决采取|会采取).{0,6}(必要|坚决|有力|一切)?.{0,4}措施|后果|玩火|自焚|不要低估|不会坐视|绝不(允许|容忍|答应)|碰.{0,2}红线|红线|死路一条|头破血流|坚决回击|坚决反制|严惩|粉碎|不惜一切|不留任何空间|将予以|必将.{0,8}(反制|回击|代价)|付出代价"}
NEG = {"en": r"lodged (stern|solemn) (representations|protests?)", "zh": r"提出严正交涉"}
_c = {k: {l: re.compile(v[l], re.I) for l in v} for k, v in [("a", ACTION), ("t", THREAT)]}
def label(sentence, lang):
    if _c["a"][lang].search(sentence): return "action"
    if _c["t"][lang].search(sentence): return "threat"
    return "neither"
