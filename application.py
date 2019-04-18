import json, pathlib, random

class Application :
    def __init__(self) :
        self.people_dic = {}
        self.worker_candidate = []

    def _show_menu(self) :
        menus = [
            "사용자 추가",
            "오늘 당번_정하기",
            "프로그램 종료"
        ]

        for i, m in enumerate(menus) :
            print("{0}. {1}".format(i + 1, m))

        n = input("메뉴 선택: ")

        try :
            n = int(n)
        except :
            print("{}은 숫자가 아닙니다".format(n))
            print()
            return self._show_menu()

        if n <= 0 or n > len(menus) :
            print("{0}은 1~{1}의 범위를 벗어나는 수입니다".format(n, len(menus)))
            print()
            return self._show_menu()
        else :
            return n

    def _add_user(self) :
        print("사용자를 추가합니다.")
        name = input("사용자의 이름을 입력해 주세요: ")

        if name not in self.people_dic.keys() :
            self.people_dic[name] = [0, 0]
        else :
            print("중복되는 사람이 있습니다.")

    def _select_people(self, people_list) :
        selection_list = []

        i = 0
        while i < 3 :
            for i, k in enumerate(people_list) :
                print("{0}. {1}".format(i + 1, k))

            numbers = input("번호로 입력해 주세요: ").split()

            for n in numbers :
                try :
                    n = int(n)
                except :
                    print("숫자가 아닙니다!")

                if n > 0 and n <= len(people_list) :
                    selection_list.append(people_list[n - 1])
                    i = 3
                else :
                    print("인덱스 범위 에러")

            i += 1

        return selection_list

    def _select_participant(self) :
        people_list = list(self.people_dic.keys())

        print("누가 당번에 참여합니까?")

        self.worker_candidate = self._select_people(people_list)

        print("{}가 참가합니다".format(self.worker_candidate))

        for name in self.worker_candidate :
            self.people_dic[name][1] += 1

    def _decide_worker(self) :
        candidate_prob = [(name, self.people_dic[name][0] / self.people_dic[name][1])
                          for name in self.worker_candidate]

        candidate_prob = sorted(candidate_prob, key=lambda x : x[1])
        print()

        min_prob = min([prob for _, prob in candidate_prob])

        for i, name_prob in enumerate(candidate_prob) :
            print("{0}. {1} - 당번률 {2}%".format(i + 1, name_prob[0], name_prob[1] * 100))

        worker = random.choice([name for name, prob in candidate_prob if prob == min_prob])
        self.people_dic[worker][0] += 1

        print("{}이(가) 당번을 맡을 차례입니다".format(worker))

    def _save_file(self) :
        file = pathlib.Path('당번.json')

        file.write_text(json.dumps(self.people_dic))

    def _load_file(self) :
        file = pathlib.Path('당번.json')

        if file.exists() :
            file_text = file.read_text()

            self.people_dic = json.loads(file_text)

    def run(self) :
        n = 0
        self._load_file()

        while n != 3 :
            n = self._show_menu()

            if n == 1 :
                self._add_user()
            elif n == 2 :
                self._select_participant()
                print()
                self._decide_worker()

            print()

        self._save_file()