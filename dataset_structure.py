""" A dictionary containing the pronouns for the expected extracted conjugations for each tense, used to check if an entry into the database has the expected structure. """

structure_dict = {
"Indicativo Presente": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Indicativo Pretérito Perfeito": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Indicativo Pretérito Imperfeito": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Indicativo Pretérito Mais-que-Perfeito": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Indicativo Pretérito Perfeito Composto": ('eu tenho', 'tu tens', 'ele/ela/você tem', 'nós temos', 'vós tendes', 'eles/elas/vocês têm'),
"Indicativo Pretérito Mais-que-Perfeito Composto": ('eu tinha', 'tu tinhas', 'ele/ela/você tinha', 'nós tínhamos', 'vós tínheis', 'eles/elas/vocês tinham'),
"Indicativo Pretérito Mais-que-Perfeito Anterior": ('eu tivera', 'tu tiveras', 'ele/ela/você tivera', 'nós tivéramos', 'vós tivéreis', 'eles/elas/vocês tiveram'),
"Indicativo Futuro do Presente Simples": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Indicativo Futuro do Presente Composto": ('eu terei', 'tu terás', 'ele/ela/você terá', 'nós teremos', 'vós tereis', 'eles/elas/vocês terão'),
"Conjuntivo / Subjuntivo Presente": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Conjuntivo / Subjuntivo Pretérito Perfeito": ('eu tenha', 'tu tenhas', 'ele/ela/você tenha', 'nós tenhamos', 'vós tenhais', 'eles/elas/vocês tenham'),
"Conjuntivo / Subjuntivo Pretérito Imperfeito": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Conjuntivo / Subjuntivo Pretérito Mais-que-Perfeito Composto": ('eu tivesse', 'tu tivesses', 'ele/ela/você tivesse', 'nós tivéssemos', 'vós tivésseis', 'eles/elas/vocês tivessem'),
"Conjuntivo / Subjuntivo Futuro": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Conjuntivo / Subjuntivo Futuro Composto": ('eu tiver', 'tu tiveres', 'ele/ela/você tiver', 'nós tivermos', 'vós tiverdes', 'eles/elas/vocês tiverem'),
"Condicional Futuro do Pretérito Simples": ('eu', 'tu', 'ele/ela/você', 'nós', 'vós', 'eles/elas/vocês'),
"Condicional Futuro do Pretérito Composto": ('eu teria', 'tu terias', 'ele/ela/você teria', 'nós teríamos', 'vós teríeis', 'eles/elas/vocês teriam'),
"Gerúndio": ("NULL",),
"Infinitivo": ("NULL", "NULL", "NULL", "NULL", "NULL"),
"Imperativo": ("NULL", "NULL", "NULL", "NULL", "NULL"), 
"Imperativo Negativo": ("NULL", "NULL", "NULL", "NULL", "NULL"),
"Particípio": ("NULL",)
}
