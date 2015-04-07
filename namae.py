# -*- coding: utf-8 -*-

import re


def split_port_name(namae_latin):
    """
    Separa as silabas, colocando vogais a mais, exatamente como na tabela de kana

    >>> split_port_name('amanda')
    ['a', 'ma', 1, 'da']
    >>> split_port_name('maria')
    ['ma', 'ri', 'a']
    >>> split_port_name('wobson')
    ['u', 'o', 'bu', 'so', 1]
    >>> split_port_name('marcos')
    ['ma', 'ru', 'ko', 'su']
    >>> split_port_name('jackson')
    ['ji', 'a', 'ki', 'so', 1]
    >>> split_port_name('fernanda')
    ['fu', 'e', 'ru', 'na', 1, 'da']
    >>> split_port_name('xucha')
    ['ji', 'u', 'ji', 'a']
    """
    # regex to split whenever it sees a vocal
    split_vocal_namae = []

    last_vogal = 0

    for item in range(0, len(namae_latin)):

        if re.match('[aeiouy]', namae_latin[item]):
            split_vocal_namae.append(namae_latin[last_vogal:item] + namae_latin[item])
            last_vogal = item + 1

    if len(namae_latin) != last_vogal:
        split_vocal_namae.append(namae_latin[last_vogal:len(namae_latin)])


    # checks the output, whenever it sees unpaired consoants, split and add an 'u' to them.
    # Watch out for the special 'n' who becomes the number '1'
    paired_u = []

    for silaba in split_vocal_namae:
        if len(silaba) == 1:
            if re.match('[aeiou]', silaba):
                paired_u.append(silaba)
            elif silaba == 'n' or silaba == 'm':
                paired_u.append(1)
            elif silaba == 'y':
                paired_u.append('i')
            else:
                paired_u.append(silaba + 'u')

        elif len(silaba) == 2:
            if silaba[0] == 'j' and silaba[1] != 'i':
                paired_u.append('ji')
                paired_u.append(silaba[1])
            elif silaba[0] == 'f' and silaba[1] != 'u':
                paired_u.append('fu')
                paired_u.append(silaba[1])
            elif silaba[0] == 'x':
                paired_u.append('ji')
                paired_u.append(silaba[1])
            elif silaba[0] == 'w':
                paired_u.append('u')
                if silaba[1] != 'u':
                    paired_u.append(silaba[1])
            elif silaba == 'ck':
                paired_u.append('ki')
            else:
                paired_u.append(silaba)

        elif len(silaba) == 3:
            if silaba[0] == silaba[1]:
                paired_u.append(silaba[1:3])
            elif silaba[0:2] == 'ch' or silaba[0:2] == 'sh':
                paired_u.append('ji')
                paired_u.append(silaba[2])
            elif silaba == 'tsu':
                paired_u.append('tu')
            else:
                if silaba[0] == 'n' or silaba[0] == 'm':
                    paired_u.append(1)
                else:
                    paired_u.append(silaba[0] + 'u')
                paired_u.append(silaba[1:3])
        elif len(silaba) == 4:
            if silaba[0:2] == 'ck':
                paired_u.append('ki')
                paired_u.append(silaba[2:4])
            else:
                paired_u.append(silaba[0] + 'u')
                paired_u.append(silaba[1] + 'u')
                paired_u.append(silaba[2:3])

    #return paired_u
    rechecked = []

    for dipolo in paired_u:
        if type(dipolo) == int:
            rechecked.append(dipolo)
        else:
            if dipolo[0] == 'j' and dipolo[1] != 'i':
                rechecked.append('ji')
                rechecked.append(dipolo[1])
            elif dipolo[0] == 'f' and dipolo[1] != 'u':
                rechecked.append('fu')
                rechecked.append(dipolo[1])
            elif dipolo[0] == 'x':
                rechecked.append('ji')
                rechecked.append(dipolo[1])
            elif dipolo[0] == 'w':
                rechecked.append('u')
                if dipolo[1] != 'u':
                    rechecked.append(dipolo[1])
            else:
                rechecked.append(dipolo)


    # substitute the letters that doesn't exist in kana, eg. co -> ko
    ordem = 0
    for dupla in rechecked:
        if dupla == 'qu':
            rechecked[ordem] = 'ku'
        elif dupla == 'ca':
            rechecked[ordem] = 'ka'
        elif dupla == 'ce':
            rechecked[ordem] = 'se'
        elif dupla == 'ci':
            rechecked[ordem] = 'si'
        elif dupla == 'co':
            rechecked[ordem] = 'ko'
        elif dupla == 'cu':
            rechecked[ordem] = 'ku'
        elif dupla == 'hu':
            rechecked[ordem] = 'u'
        elif type(dupla) != int and len(dupla) == 2:
            if dupla[1] == 'ly':
                rechecked[ordem] = 'ri'
            elif dupla[1] == 'y' and dupla[0] != 'l':
                rechecked[ordem] = dupla[0] + 'i'
            elif dupla[0] == 'l':
                rechecked[ordem] = 'r' + dupla[1]

        ordem += 1

    namae_splitted = rechecked

    return namae_splitted


def namae_to_hiragana(namae_splitted):
    """
    Converte o nome escrito em letras latinas em hiragana

    >>> namae_to_hiragana(['a', 'ma', 1, 'da'])
    u'\u3042\u307e\u3093\u3060'
    >>> namae_to_hiragana(['ma', 'ru', 'ko', 'su'])
    u'\u307e\u308b\u3053\u3059'
    """

    kana_table = {

        'a': u'あ',
        'e': u'え',
        'i': u'い',
        'o': u'お',
        'u': u'う',
        'y': u'い',

        1: u'ん',

        'ka': u'か',
        'ki': u'き',
        'ku': u'く',
        'ke': u'け',
        'ko': u'こ',

        'ga': u'が',
        'gi': u'ぎ',
        'gu': u'ぐ',
        'ge': u'げ',
        'go': u'ご',

        'sa': u'さ',
        'se': u'せ',
        'si': u'し',
        'so': u'そ',
        'su': u'す',

        'za': u'ざ',
        'ze': u'ぜ',
        'ji': u'じ',
        'zo': u'ぞ',
        'zu': u'ず',

        'ta': u'た',
        'te': u'て',
        'ti': u'ち',
        'to': u'と',
        'tu': u'つ',

        'da': u'だ',
        'de': u'で',
        'di': u'ぢ',
        'do': u'ど',
        'du': u'づ',

        'ma': u'ま',
        'me': u'め',
        'mi': u'み',
        'mo': u'も',
        'mu': u'む',

        'ha': u'は',
        'he': u'へ',
        'hi': u'ひ',
        'ho': u'ほ',
        'fu': u'ふ',

        'ba': u'ば',
        'be': u'べ',
        'bi': u'び',
        'bo': u'ぼ',
        'bu': u'ぶ',

        'pa': u'ぱ',
        'pe': u'ぺ',
        'pi': u'ぴ',
        'po': u'ぽ',
        'pu': u'ぷ',

        'na': u'な',
        'ne': u'ね',
        'ni': u'に',
        'no': u'の',
        'nu': u'ぬ',

        'ra': u'ら',
        're': u'れ',
        'ri': u'り',
        'ro': u'ろ',
        'ru': u'る',

        'ya': u'や',
        'yu': u'ゆ',
        'yo': u'よ',
        'wa': u'わ'



    }

    namae_hiragana = ''

    for silaba in namae_splitted:
        namae_hiragana += kana_table[silaba]

    return namae_hiragana





def namae_to_katakana(namae_hiragana):
    """
    Converte o nome escrito em hiragana em katakana

    >>> namae_to_katakana(u'\u3042\u307e\u3093\u3060')
    u'\u30a2\u30de\u30f3\u30c0'
    >>> namae_to_katakana(u'\u307e\u308b\u3053\u3059')
    u'\u30de\u30eb\u30b3\u30b9'

    """

    kata_table = {

        u'あ': u'ア',
        u'え': u'エ',
        u'い': u'イ',
        u'お': u'オ',
        u'う': u'ウ',

        u'ん': u'ン',


        u'か': u'カ',
        u'き': u'キ',
        u'く': u'ク',
        u'け': u'ケ',
        u'こ': u'コ',

        u'が': u'ガ',
        u'ぎ': u'ギ',
        u'ぐ': u'グ',
        u'げ': u'ゲ',
        u'ご': u'ゴ',

        u'さ': u'サ',
        u'せ': u'セ',
        u'し': u'シ',
        u'そ': u'ソ',
        u'す': u'ス',

        u'ざ': u'ザ',
        u'ぜ': u'ゼ',
        u'じ': u'ジ',
        u'ぞ': u'ゾ',
        u'ず': u'ズ',

        u'た': u'タ',
        u'て': u'テ',
        u'ち': u'チ',
        u'と': u'ト',
        u'つ': u'ツ',

        u'だ': u'ダ',
        u'で': u'デ',
        u'ぢ': u'ヂ',
        u'ど': u'ド',
        u'づ': u'ヅ',

        u'ま': u'マ',
        u'め': u'メ',
        u'み': u'ミ',
        u'も': u'モ',
        u'む': u'ム',

        u'は': u'ハ',
        u'へ': u'ヘ',
        u'ひ': u'ヒ',
        u'ほ': u'ホ',
        u'ふ': u'フ',

        u'ば': u'バ',
        u'べ': u'ベ',
        u'び': u'ビ',
        u'ぼ': u'ボ',
        u'ぶ': u'ブ',

        u'ぱ': u'パ',
        u'ぺ': u'ペ',
        u'ぴ': u'ピ',
        u'ぽ': u'ポ',
        u'ぷ': u'プ',

        u'な': u'ナ',
        u'ね': u'ネ',
        u'に': u'ニ',
        u'の': u'ノ',
        u'ぬ': u'ヌ',

        u'ら': u'ラ',
        u'れ': u'レ',
        u'り': u'リ',
        u'ろ': u'ロ',
        u'る': u'ル',

        u'や': u'ヤ',
        u'ゆ': u'ユ',
        u'よ': u'ヨ',
        u'わ': u'ワ'

    }


    namae_in_katakana = ''

    for character in namae_hiragana:
        namae_in_katakana += kata_table[character]

    return namae_in_katakana

def namae_to_kanji(namae_hiragana):
    """
    Converte o nome escrito em hiragana em kanji

    >>> namae_to_kanji(u'\u3042\u307e\u3093\u3060')
    u''
    >>> namae_to_kanji(u'\u307e\u308b\u3053\u3059')
    u''
    """

    kanji_table = {

        u'あ': u'亜',
        u'え': u'江',
        u'い': u'伊',
        u'お': u'於',
        u'う': u'宇',

        u'ん': u'運',


        u'か': u'河',
        u'き': u'喜',
        u'く': u'玖',
        u'け': u'毛',
        u'こ': u'古',

        u'が': u'賀',
        u'ぎ': u'宜',
        u'ぐ': u'具',
        u'げ': u'下',
        u'ご': u'伍',

        u'さ': u'佐',
        u'せ': u'世',
        u'し': u'志',
        u'そ': u'祖',
        u'す': u'寿',

        u'ざ': u'座',
        u'ぜ': u'是',
        u'じ': u'治',
        u'ぞ': u'蔵',
        u'ず': u'図',

        u'た': u'田',
        u'て': u'手',
        u'ち': u'知',
        u'と': u'戸',
        u'つ': u'通',

        u'だ': u'惰',
        u'で': u'出',
        u'ぢ': u'地',
        u'ど': u'土',
        u'づ': u'津',

        u'ま': u'真',
        u'め': u'眼',
        u'み': u'魅',
        u'も': u'謨',
        u'む': u'眸',

        u'は': u'羽',
        u'へ': u'部',
        u'ひ': u'火',
        u'ほ': u'浦',
        u'ふ': u'符',

        u'ば': u'場',
        u'べ': u'辺',
        u'び': u'美',
        u'ぼ': u'菩',
        u'ぶ': u'豊',

        u'ぱ': u'巴',
        u'ぺ': u'遍',
        u'ぴ': u'比',
        u'ぽ': u'保',
        u'ぷ': u'布',

        u'な': u'奈',
        u'ね': u'根',
        u'に': u'仁',
        u'の': u'野',
        u'ぬ': u'塗',

        u'ら': u'羅',
        u'れ': u'列',
        u'り': u'理',
        u'ろ': u'路',
        u'る': u'流',

        u'や': u'',
        u'ゆ': u'',
        u'よ': u'',
        u'わ': u'和'

    }


    namae_in_kanji = ''

    for character in namae_hiragana:
        namae_in_kanji += kanji_table[character]

    return namae_in_kanji



def nipo_name(namae_latin):
    # return name in kana and kanji, calling other functions
    namae_splitted = split_port_name(namae_latin)
    namae_hiragana = namae_to_hiragana(namae_splitted)
    namae_katakana = namae_to_katakana(namae_hiragana)
    namae_kanji = namae_to_kanji(namae_hiragana)

    return [namae_hiragana, namae_katakana, namae_kanji]



#def main():
#
#    pass
