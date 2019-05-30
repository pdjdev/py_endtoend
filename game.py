#명령 프롬프트에서 pip install requests로 웹요청 모듈 설치
import requests, hgtk, random

#이미 있는 단어 알기위해 단어목록 저장
history = []
playing = True

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

def findword(char):
    url = 'https://krdict.korean.go.kr/api/search?key=[APIKEY]&part=word&pos=1&q=' + char + '*'
    response = requests.get(url)
    ans = []
    #단어 목록을 불러오기
    words = midReturn_all(response.text,'<item>','</item>')
    for w in words:
        word = midReturn(w, '<word>', '</word>') #단어 불러오기
        pos = midReturn(w, '<pos>', '</pos>') #품사 불러오기
        
        #이미 쓴 단어가 아닐때
        if not (w in history):
            
            #한글자가 아니고 품사가 명사일때
            if len(word) > 1 and pos == '명사' and not word in history:
                ans.append(word)

    if len(ans)>0:
        return random.choice(ans)
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
        query = input('나>')
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
                if hgtk.letter.decompose(sword)[0] == 'ㄹ' and hgtk.letter.decompose(query[0])[0] == 'ㄴ':
                    print('두음법칙 적용됨')
                elif hgtk.letter.decompose(sword)[0] == 'ㄴ' and hgtk.letter.decompose(query[0])[0] == 'ㅇ':
                    print('두음법칙 적용됨')
                else:
                    wordOK = False
                    print(sword + '(으)로 시작하는 단어여야 합니다.')
                
            if len(query) == 1:
                wordOK = False
                print('적어도 두 글자가 되어야 합니다')

            if query in history:
                wordOK = False
                print('이미 입력한 단어입니다')

            if wordOK:
                #단어의 유효성을 체크
                url = 'https://krdict.korean.go.kr/api/search?key=5952ED12C2378685A8F4087BCD0398F7&part=word&pos=1&q=' + query
                response = requests.get(url)
                #단어 목록을 불러오기
                words = midReturn_all(response.text, '<word>', '</word>') #단어 불러오기
                #검색 결과에 쿼리가 존재할때
                actualWords = False
                for w in words:
                    if w == query: actualWords = True
                if not actualWords:
                    wordOK = False
                    print('유효한 단어를 입력해 주십시오')
                    

    history.append(query)
    
    if playing:       
        start = query[len(query)-1]

        ans = findword(start)

        if ans=='':
            #두음법칙 적용하여 재검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄹ':
               newq = hgtk.letter.compose('ㅇ', sdis[1], sdis[2])
               print(start, '->', newq)
               ans = findword(newq)

        if ans=='':
            #두음법칙 적용하여 재검색
            sdis = hgtk.letter.decompose(start)
            if sdis[0] == 'ㄹ':
               newq = hgtk.letter.compose('ㄴ', sdis[1], sdis[2])
               print(start, '->', newq)
               ans = findword(newq)
            
        if ans=='':
            print('당신의 승리!')
            break
        else:
            history.append(ans)
            print('컴퓨터>', ans)
            sword = history[len(history)-1][len(history[len(history)-1])-1]
            
            #컴퓨터 승리여부 체크            
            #if findword(sword) == '':
            #    print('tip: \'/다시\'를 입력하여 게임을 다시 시작할 수 있습니다')

            
            

