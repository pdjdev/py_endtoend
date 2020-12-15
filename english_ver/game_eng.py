import random

history = [] #사용된 단어 목록을 저장하는 리스트
playing = True #게임 상태를 나타내는 변수. False가 되면 게임을 중단함
hasReply = False #컴퓨터로부터 답장을 받은적 있는지 체크함.

def findword(query): #컴퓨터가 답장할 단어를 찾는 함수
    with open('words_alpha.txt') as data:
        lines = data.readlines()
    suitable_lists = [] #조건에 맞는 단어들의 리스트
    i = 0
    for i in range(len(lines)):
        if query[len(query)-2] == lines[i][0] and query[len(query)-1] == lines[i][1]: #query의 첫번째와 두번째 글자가 lines의 첫번째와 두번째 글자와 같으면
            suitable_lists.append(lines[i]) #suitable_lists에 추가함

    computer_answer = random.choice(suitable_lists) #random 함수를 이용하여 suitable_lists의 요소중 하나를 답장으로 정함
    start_word = computer_answer[len(computer_answer)-3] + computer_answer[len(computer_answer)-2] #끝말 2글자를 추출해 사용자가 답장해야 할 앞 글자 2개를 저장함

    if len(suitable_lists) > 0:
        history.append(computer_answer) #컴퓨터의 답장을 history에 추가함
        return computer_answer
    else:
        return ''

def checkexists(query): #입력한 단어가 words_alpha.txt에 존재하는지 검색하는 함수

    with open('words_alpha.txt') as data:
        lines = data.readlines()

    #단어 목록을 불러옴
    words = lines

    w = 0
    count = 0

    for w in range(len(lines)):
        if (query + '\n' == words[w]): #일치하는 단어가 words_alpha.txt에 있으면 count를 증가시킴
            count = count + 1

    if count != 0:
        return True
    else:
        return False

print('''
=============영어 끝맛잇기=============
- - - 게임 방법 - - -
먼저 단어를 입력하면 끝말잇기가 시작됩니다.
'/그만'을 입력하면 게임이 종료되며, '/다시'를 입력하여 게임을 다시 시작할 수 있습니다.

- - - 게임 규칙 - - -
1. 단어의 길이가 적어도 두 글자 이상이어야 합니다.
2. 이미 사용한 단어를 다시 사용할 수 없습니다.
3. words_alpha.txt 파일에 있는 단어여야 합니다.(웬만한 단어는 다 있습니다.)
'''
)

print('게임을 시작합니다.')

while(playing):
    wordOK = False

    while (not wordOK):
        query = input('> ')
        wordOK = True

        if query == '/stop': #게임을 중지함
            playing = False
            print('Computer win!')
            break
        elif query == '/restart': #게임을 재시작함
            history = []
            print('Restart the game')
            wordOK = False
        else:
            if query == '':
                wordOK = False

                if len(history) == 0:
                    print('단어를 입력하여 끝말잇기를 시작합니다.')
                else:
                    print(findword().start_word + '(으)로 시작하는 단어를 입력해 주십시오.')

            else:
                if len(query) == 1: #글자 수가 1일시
                    print('적어도 두 글자가 되어야 합니다.')
                    continue

                if query in history: #이미 사용된 단어일 경우
                    print('이미 사용된 단어입니다.')
                    continue

                if len(history)>0 and hasReply == True: #이미 답장이 온 경우에만 끝말을 추출할 수 있기 때문에 hasReply을 사용함
                    if query[0] != com_answer[len(com_answer)-3] or query[1] != com_answer[len(com_answer)-2]:
                        print(com_answer[len(com_answer)-3] + com_answer[len(com_answer)-2] + '(으)로 시작하는 단어여야 합니다.')
                        continue

                isExist = checkexists(query) #단어가 words_alpha.txt에 있는지 확인함

                if isExist == False:
                    print('유효한 단어를 입력해주세요.')
                    continue

                com_answer = findword(query)

                print(query, '->', com_answer)
                hasReply = True

                if com_answer == '':
                    print('You Win!')
                    break

    history.append(query)