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

"""
# An Example of a text_dataset scraped from https://conjugator.reverso.net/conjugation-portuguese-verb-poder.html.

Indicativo Presente
('eu', 'posso', True)
('tu', 'podes', False)
('ele/ela/você', 'pode', False)     
('nós', 'podemos', False)
('vós', 'podeis', False)
('eles/elas/vocês', 'podem', False) 

Indicativo Pretérito Perfeito       
('eu', 'pude', True)
('tu', 'pudeste', True)
('ele/ela/você', 'pôde', True)      
('nós', 'pudemos', True)
('vós', 'pudestes', True)
('eles/elas/vocês', 'puderam', True)

Indicativo Pretérito Imperfeito     
('eu', 'podia', False)
('tu', 'podias', False)
('ele/ela/você', 'podia', False)    
('nós', 'podíamos', False)
('vós', 'podíeis', False)
('eles/elas/vocês', 'podiam', False)

Indicativo Pretérito Mais-que-Perfeito
('eu', 'pudera', True)
('tu', 'puderas', True)
('ele/ela/você', 'pudera', True)
('nós', 'pudéramos', True)
('vós', 'pudéreis', True)
('eles/elas/vocês', 'puderam', True)

Indicativo Pretérito Perfeito Composto
('eu tenho', 'podido', False)
('tu tens', 'podido', False)
('ele/ela/você tem', 'podido', False)
('nós temos', 'podido', False)
('vós tendes', 'podido', False)
('eles/elas/vocês têm', 'podido', False)

Indicativo Pretérito Mais-que-Perfeito Composto
('eu tinha', 'podido', False)
('tu tinhas', 'podido', False)
('ele/ela/você tinha', 'podido', False)
('nós tínhamos', 'podido', False)
('vós tínheis', 'podido', False)
('eles/elas/vocês tinham', 'podido', False)

Indicativo Pretérito Mais-que-Perfeito Anterior
('eu tivera', 'podido', False)
('tu tiveras', 'podido', False)
('ele/ela/você tivera', 'podido', False)
('nós tivéramos', 'podido', False)
('vós tivéreis', 'podido', False)
('eles/elas/vocês tiveram', 'podido', False)

Indicativo Futuro do Presente Simples
('eu', 'poderei', False)
('tu', 'poderás', False)
('ele/ela/você', 'poderá', False)
('nós', 'poderemos', False)
('vós', 'podereis', False)
('eles/elas/vocês', 'poderão', False)

Indicativo Futuro do Presente Composto
('eu terei', 'podido', False)
('tu terás', 'podido', False)
('ele/ela/você terá', 'podido', False)
('nós teremos', 'podido', False)
('vós tereis', 'podido', False)
('eles/elas/vocês terão', 'podido', False)

Conjuntivo / Subjuntivo Presente
('eu', 'possa', True)
('tu', 'possas', True)
('ele/ela/você', 'possa', True)
('nós', 'possamos', True)
('vós', 'possais', True)
('eles/elas/vocês', 'possam', True)

Conjuntivo / Subjuntivo Pretérito Perfeito
('eu tenha', 'podido', False)
('tu tenhas', 'podido', False)
('ele/ela/você tenha', 'podido', False)
('nós tenhamos', 'podido', False)
('vós tenhais', 'podido', False)
('eles/elas/vocês tenham', 'podido', False)

Conjuntivo / Subjuntivo Pretérito Imperfeito
('eu', 'pudesse', True)
('tu', 'pudesses', True)
('ele/ela/você', 'pudesse', True)
('nós', 'pudéssemos', True)
('vós', 'pudésseis', True)
('eles/elas/vocês', 'pudessem', True)

Conjuntivo / Subjuntivo Pretérito Mais-que-Perfeito Composto
('eu tivesse', 'podido', False)
('tu tivesses', 'podido', False)
('ele/ela/você tivesse', 'podido', False)
('nós tivéssemos', 'podido', False)
('vós tivésseis', 'podido', False)
('eles/elas/vocês tivessem', 'podido', False)

Conjuntivo / Subjuntivo Futuro
('eu', 'puder', True)
('tu', 'puderes', True)
('ele/ela/você', 'puder', True)
('nós', 'pudermos', True)
('vós', 'puderdes', True)
('eles/elas/vocês', 'puderem', True)

Conjuntivo / Subjuntivo Futuro Composto
('eu tiver', 'podido', False)
('tu tiveres', 'podido', False)
('ele/ela/você tiver', 'podido', False)
('nós tivermos', 'podido', False)
('vós tiverdes', 'podido', False)
('eles/elas/vocês tiverem', 'podido', False)

Condicional Futuro do Pretérito Simples
('eu', 'poderia', False)
('tu', 'poderias', False)
('ele/ela/você', 'poderia', False)
('nós', 'poderíamos', False)
('vós', 'poderíeis', False)
('eles/elas/vocês', 'poderiam', False)

Condicional Futuro do Pretérito Composto
('eu teria', 'podido', False)
('tu terias', 'podido', False)
('ele/ela/você teria', 'podido', False)
('nós teríamos', 'podido', False)
('vós teríeis', 'podido', False)
('eles/elas/vocês teriam', 'podido', False)

Gerúndio
(None, 'podendo', False)

Infinitivo
(None, 'poder', False)
(None, 'poderes', False)
(None, 'podermos', False)
(None, 'poderdes', False)
(None, 'poderem', False)

Imperativo
(None, 'pode', False)
(None, 'possa', True)
(None, 'possamos', True)
(None, 'podei', False)
(None, 'possam', True)

Imperativo Negativo
(None, 'possas', True)
(None, 'possa', True)
(None, 'possamos', True)
(None, 'possais', True)
(None, 'possam', True)

Particípio
(None, 'podido', False)

"""