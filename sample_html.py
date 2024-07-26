# Sample html scenarios used for testing.

html_dict = {
"html_tense": """
    <div id="ch_divSimple" class="word-wrap-simple">
        <div class="result-block-api">
            <div class="word-wrap-row">
                <div class="word-wrap-title">
                    <h4>Indicativo</h4>
                </div>
                    <div class="wrap-three-col">
                        <div class="blue-box-wrap" mobile-title="Indicativo Presente">
                    </div>
            </div>
        </div>
    </div>
""",
"html_tense_pronoun_conjugation" : """
    <div id="ch_divSimple" class="word-wrap-simple">
        <div class="result-block-api">
            <div class="word-wrap-row">
                <div class="word-wrap-title">
                    <h4>Indicativo</h4>
                </div>
                    <div class="wrap-three-col">
                        <div class="blue-box-wrap" mobile-title="Indicativo Presente">
                            <p>Presente</p>
                            <ul class="wrap-verbs-listing">
                                <li>
                                    <i class="graytxt">eu</i>
                                    <i h="1">
                                        <i class="verbtxt">t</i>
                                        <i class="verbtxt-term-irr">enho</i>
                                    </i>
                                </li>
                            </ul>
                        </div>
                    </div> 
            </div> 
        </div> 
    </div> 
""",
"html_tense_aux_pronoun_conjugation" : """ 
<div class="blue-box-wrap" mobile-title="Indicativo Pretérito Perfeito Composto">
    <p>Pretérito Perfeito Composto</p>
    <ul class="wrap-verbs-listing">
        <li>
            <i class="graytxt">eu</i>
            <i class="auxgraytxt">tenho</i>
            <i h="1">
                <i class="verbtxt">t</i>
                <i class="verbtxt-term">ido</i>
            </i>
        </li>
    </ul>
</div> 
""",
"html_wrong_class" : """
<div id="ch_divSimple" class="word-wrap-simple">
    <div class="result-block-api">
        <div class="word-wrap-row">
            <div class="word-wrap-title">
                <h4>Indicativo</h4>
            </div>
                <div class="wrap-three-col">
                    <div class="RED-box-wrap" mobile-title="Indicativo Presente">
                </div>
        </div>
    </div>
</div>
""",
"html_multiple_tags": """
<div class="wrap-three-col">
    <div class="blue-box-wrap" mobile-title="Condicional Futuro do Pretérito Simples">
        <p>Futuro do Pretérito Simples</p>
        <ul class="wrap-verbs-listing">
            <li>
                <i class="graytxt">eu</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eria</i>
                </i>
            </li>
            <li>
                <i class="graytxt">tu</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">erias</i>
                </i>
            </li>
            <li>
                <i class="graytxt">ele/ela/você</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eria</i>
                </i>
            </li>
            <li>
                <i class="graytxt">nós</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eríamos</i>
                </i>
            </li>
            <li>
                <i class="graytxt">vós</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eríeis</i>
                </i>
            </li>
            <li>
                <i class="graytxt">eles/elas/vocês</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eriam</i>
                </i>
            </li>
        </ul>
    </div>
</div>
""",
"html_multiple_tags_tense_only": """
<div class="blue-box-wrap" mobile-title="Gerúndio">
    <ul class="wrap-verbs-listing top2">
        <li>
            <i h="1">
                <i class="verbtxt">t</i>
                <i class="verbtxt-term">endo</i>
            </i>
        </li>
    </ul>
</div>
<div class="blue-box-wrap" mobile-title="Particípio">
    <ul class="wrap-verbs-listing top3">
        <li>
            <i h="1">
                <i class="verbtxt">t</i>
                <i class="verbtxt-term">ido</i>
            </i>
        </li>
    </ul>
</div>
""",
"html_multiple_tags_missing_tense": """
<div class="wrap-three-col">
    <div class="blue-box-wrap" mobile-title="Condicional Futuro do Pretérito Simples">
        <p>Futuro do Pretérito Simples</p>
        <ul class="wrap-verbs-listing">
            <li>
                <i class="graytxt">eu</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eria</i>
                </i>
            </li>
            <li>
                <i class="graytxt">tu</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">erias</i>
                </i>
            </li>
            <li>
                <i class="graytxt">ele/ela/você</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eria</i>
                </i>
            </li>
            <li>
                <i class="graytxt">nós</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eríamos</i>
                </i>
            </li>
            <li>
                <i class="graytxt">vós</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eríeis</i>
                </i>
            </li>
            <li>
                <i class="graytxt">eles/elas/vocês</i>
                <i h="1">
                    <i class="verbtxt">t</i>
                    <i class="verbtxt-term">eriam</i>
                </i>
            </li>
        </ul>
    </div>
</div>
"""
}


