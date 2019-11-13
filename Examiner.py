from selenium import webdriver
import time
import AnswerModel


def autoLogin(uid, password, code):
    al_account = driver.find_element_by_name('login1$txtName')
    al_account.clear()
    al_account.send_keys(uid)

    al_password = driver.find_element_by_name('login1$txtPwd')
    al_password.clear()
    al_password.send_keys(password)

    al_code = driver.find_element_by_name('login1$txt_Code')
    al_code.clear()
    al_code.send_keys(code)

    al_code = driver.find_element_by_name('login1$Btn_Login')
    al_code.click()


def doTestExam():
    elements = driver.find_elements_by_tag_name("b")
    problemName = elements[0]
    problemName = problemName.text[problemName.text.find("、") + 1:]
    choices = elements[1:]
    print(problemName)
    try:
        problemAnswerIndex = answersProblemName.index(problemName)
    except:
        print("Error: can't index!")
        return
    problemAnswer = answers[problemAnswerIndex][1]
    print("answer:" + problemAnswer)

    inputs = driver.find_elements_by_tag_name("input")
    radios = []
    for input_item in inputs:
        if input_item.get_attribute("type") == "radio" or input_item.get_attribute("type") == "checkbox":
            radios.append(input_item)
    choose_list = []
    for iid, choice in enumerate(choices):
        print(choice.text, problemAnswer)
        if choice.text == problemAnswer:  # 单选题
            choose_list.append(iid)
            print("Add Click:" + str(iid))
        if problemAnswer.find(choice.text[:choice.text.find("、")]) != -1:  # 单选题&多选题
            choose_list.append(iid)
            print("Add Click:" + str(iid))

    for need_choose in choose_list:
        radios[need_choose].click()
        print("Do Click:" + str(need_choose))
        time.sleep(0.2)
    buttonOK = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnOk")
    buttonOK.click()
    time.sleep(0.5)
    buttonNext = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnNext")
    buttonNext.click()


def doExam():
    answer_question = driver.find_elements_by_id("Table2")
    for question in answer_question:
        problemName = question.find_element_by_tag_name("span")
        problemName = problemName.text[problemName.text.find("、") + 1:]
        print(problemName)
        try:
            problemAnswerIndex = answersProblemName.index(problemName)
        except:
            print("Error: can't index!")
            continue
        problemAnswer = answers[problemAnswerIndex][1]
        print("answer:" + problemAnswer)

        inputs = question.find_elements_by_tag_name("input")
        labels = question.find_elements_by_tag_name("label")
        choose_list = []
        for iid, answer_choice in enumerate(labels):
            print(answer_choice.text)
            if problemAnswer.find(answer_choice.text[answer_choice.text.find("、") + 1:]) != -1:  # 判断题
                choose_list.append(iid)
                print("Add Clicks:" + str(iid))
            if problemAnswer.find(answer_choice.text[:answer_choice.text.find("、")]) != -1:  # 单选题&多选题
                choose_list.append(iid)
                print("Add Clicks:" + str(iid))
        for need_choose in choose_list:
            try:
                inputs[need_choose].click()
                if not inputs[need_choose].is_selected():
                    print("Error: Can't click! Please click #" + str(need_choose) + "# by hand and press enter to go on")
                    input()
                    continue
                print("Do Click:" + str(need_choose))
                time.sleep(0.2)
            except:
                print("Error: Can't click! Please click #" + str(need_choose) +"# by hand and press enter to go on")
                input()

        # buttonOK = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnOk")
        # buttonOK.click()


if __name__ == "__main__":
    # 打印使用方法
    print("软件使用方法:")
    print("login [学号] [验证码] 自动填写账号密码验证码")
    print("test [做题数] 做测试题")
    print("exam 做考试题")
    print("title 查看当前窗口标题")
    print("window 查看所有窗口")
    print("switch [窗口ID] 切换至指定窗口")
    print("quit 退出")

    # init Examiner
    driver = webdriver.Chrome()
    answers = AnswerModel.AnswerCSVToList("answerlist.csv")
    answersProblemName = []
    driver.get("http://sys.xtu.edu.cn/aqzr/")
    for index, answer in enumerate(answers):
        answers[index][0] = answer[0][answer[0].find("、") + 1:]
        answersProblemName.append(answers[index][0])

    while True:
        command_raw = input()
        command = command_raw.split(" ")
        #
        if command[0] == "test":
            try:
                for i in range(1, 1 + int(command[1])):
                    doTestExam()
                    time.sleep(0.5)
                print("做测试题 完毕")
            except:
                print("命令输入错误: test [做题数] 或 未切换至对应窗口")
        if command[0] == "exam":
            doExam()
            print("做考试题 完毕")
        if command[0] == "login":
            autoLogin(command[1], command[1], command[2])
            print("登录成功")
        if command[0] == "window":
            print(driver.window_handles)
        if command[0] == "title":
            print(driver.title)
        if command[0] == "switch":
            try:
                driver.switch_to.window(driver.window_handles[int(command[1])])
                print("切换到:" + str(driver.window_handles[int(command[1])]))
            except:
                print("切换失败")
        if command[0] == "quit":
            quit()