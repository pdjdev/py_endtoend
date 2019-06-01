#pip install requests hgtk
import requests, hgtk, random

#이미 있는 단어 알기위해 단어목록 저장
history = []
playing = True
#키 발급은 https://krdict.korean.go.kr/openApi/openApiInfo
apikey = ''

#좀 치사한 한방단어 방지 목록
blacklist = ['즘', '틱', '늄', '슘', '퓸', '늬', '뺌', '섯', '숍']

#지정한 두 개의 문자열 사이의 문자열을 리턴하는 함수
#string list에서 단어, 품사와 같은 요소들을 추출할때 사용됩니다
def midReturn(val, s, e):
    if s in val:
        val = val[val.find(s)+len(s):]
        if e in val: val = val[:val.find(e)]
    return val

#지정한 두 개의 문자열 사이의 문자열 여러개를 리턴하는 함수
#string에서 XML 등의 요소를 분석할때 사용됩니다
def midReturn_all(val, s, e):
    if s in val:
        tmp = val.split(s)
        val = []
        for i in range(0, len(tmp)):
            if e in tmp[i]: val.append(tmp[i][:tmp[i].find(e)])
    else:
        val = []
    return val

def findword(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url)
    ans = []
    
    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        #이미 쓴 단어가 아닐때
        if not (w in history):           
            #한글자가 아니고 품사가 명사일때
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and not word in history and not word[len(word)-1] in blacklist:
                ans.append(w)
    if len(ans)>0:
        return random.choice(ans)
    else:
        return ''


def checkexists(query):
    url = 'https://krdict.korean.go.kr/api/search?key=' + apikey + '&part=word&pos=1&q=' + query
    response = requests.get(url)
    ans = ''

    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        #이미 쓴 단어가 아닐때
        if not (w in history):           
            #한글자가 아니고 품사가 명사일때
            word = midReturn(w,'<word>','</word>')
            pos = midReturn(w,'<pos>','</pos>')
            if len(word) > 1 and pos == '명사' and word == query: ans = w

    if len(ans)>0:
        return ans
    else:
        return ''


print('''
=============파이썬 끝말잇기===============

사전 데이터 제공: 국립국어원 한국어기초사전

- - - 게임 방법 - - -
가장 처음 단어를 제시하면 끝말잇기가 시작됩니다
'/그만'을 입력하면 게임이 종료되며, '/다시'를 입력하여 게임을 다시 시작할 수 있습니다.

- - - 게임 규칙 - - -
1. 사전에 등재된 명사여야 합니다
2. 적어도 단어의 길이가 두 글자 이상이어야 합니다
3. 이미 사용한 단어를 다시 사용할 수 없습니다
4. 두음법칙 적용 가능합니다 (ex. 리->니)

==========================================
''')

while(playing):

    wordOK = False

    while(not wordOK):
        query = input('나> ')
        wordOK = True
        
        if query == '/그만':
            playing = False
            break
        elif query == '/다시':
            history = []
            print('게임을 다시 시작합니다.')
            wordOK = False
        else:         
            if query == '':
                wordOK = False

                if len(history)==0:
                    print('단어를 입력하여 끝말잇기를 시작합니다.')
                else:
                    print(sword + '(으)로 시작하는 단어를 입력해 주십시오.')
            
            #첫 글자의 초성 분석하여 두음법칙 적용 -> 규칙에 아직 완벽하게 맞지 않으므로 차후 수정 필요
            if not len(history)==0 and not query[0] == sword and not query=='':
                sdis = hgtk.letter.decompose(sword)
                qdis = hgtk.letter.decompose(query[0])
                if sdis[0] == 'ㄹ' and qdis[0] == 'ㄴ': print('두음법칙 적용됨')
                elif sdis[0] == 'ㄹ' and qdis[0] == 'ㅇ' and qdis[1] in ('ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'): print('두음법칙 적용됨')
                else:
                    wordOK = False
                    print(sword + '(으)로 시작하는 단어여야 합니다.')
                
            if len(query) == 1:
                wordOK = False
                print('적어도 두 글자가 되어야 합니다')

            if query in history:
                wordOK = False
                print('이미 입력한 단어입니다')

            if query[len(query)-1] in blacklist:
                print('아.. 좀 치사한데요..')

            if wordOK:
                #단어의 유효성을 체크
                ans = checkexists(query)
                if ans == '':
                    wordOK = False
                    print('유효한 단어를 입력해 주십시오')
                else:
                    print('(' + midReturn(ans, '<definition>', '</definition>') + ')\n')
                    
    history.append(query)
    
    if playing:       
        start = query[len(query)-1]

        ans = findword(start + '*')

        if ans=='':
            #ㄹ -> ㄴ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄹ':
               newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
               print(start, '->', newq)
               start = newq
               ans = findword(newq + '*')

        if ans=='':
            #(ㄹ->)ㄴ -> ㅇ 검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄴ' and sdis[1] in ('ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ'):
                newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
                print(start, '->', newq)
                ans = findword(newq + '*')
            
        if ans=='':
            print('당신의 승리!')
            break
        else:
            answord = midReturn(ans, '<word>', '</word>') #단어 불러오기
            ansdef = midReturn(ans, '<definition>', '</definition>') #품사 불러오기
            history.append(answord)
            
            print('컴퓨터>', answord, '\n('+ansdef+')\n')
            sword = history[len(history)-1][len(history[len(history)-1])-1]
            
            #컴퓨터 승리여부 체크            
            #if findword(sword) == '':
            #    print('tip: \'/다시\'를 입력하여 게임을 다시 시작할 수 있습니다')
            
