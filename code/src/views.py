import erniebot
import json


# def index(request):
#     return render(request, 'index.html')

#如果只针对想要调用文心一言的话，不需要使用Django包（这个是用来搭后端的，调用不需要用到）
#这个ask方法是可以正常用了，已经调用成功获取到结果了，不过json解析那里有点问题，
def ask():

    # 从txt文件中读取内容
    txt_file_path = '../img/result/txts/combined_text.txt'
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        question = file.read()

    # 配置 ErnieBot 的 API 类型、访问令牌和模型名称
    erniebot.api_type = 'aistudio'
    erniebot.access_token = "47ff222f7ca92adbfab5cccf59c8bf7b4e46b3fc"
    model = 'ernie-bot'

    # 将文本放在单个消息对象中，用空格分隔不同的文本段落
    message_content = " 以下是一篇高中作文，自命题作文 " \
        f"- 我需要你以一个老师的角色来批阅这篇作文{question} " \
        "- 完成五个任务，第一个是打分（满分为60），第二个是生成评语，评语既要肯定好的地方也要指出不足，第三个是润色一些语句（给出原句和润色后），第四个是推荐作文想提高可以参照的知识点，第五个是根据这些知识点推荐网课 " \
        "- 推荐作文想提高可以参照的知识点部分，比如说如果修辞手法不够，就推荐修辞手法；文章结构不清晰，就推荐文章结构；没有语言风格，就推荐语言风格  " \
        "- The output is just pure JSON format, with no other descriptions." \
        "- Please strictly answer according to the following statements, without extra words. " \
        "- 示例json文件如下，参考格式：[{\"基于文心大模型的打分\": \"\", \"评语\":\"\", \"润色的语句\":\"\",\"可以参照的知识点\": \"\", \"推荐的网课\":\"\",},] "\
        "- 评语在100个中文汉字左右。 " \
        "- 推荐作文想提高可以参照的知识点个数在3-5个"
    # 构建对话消息
    messages = [
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content
        }
    ]

    # 调用文心一言回答问题
    response = erniebot.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    # 获取文心一言的回答
    answer = response.result

    # 解析json
    try:
        json_start = answer.find("[")
        json_end = answer.rfind("]")
        if json_start != -1 and json_end != -1:
            json_content = answer[json_start:json_end+1]
            answer_dict = json.loads(json_content)
        else:
            answer_dict = {}
            # 使用json.dumps进行漂亮的打印
            print(json.dumps(answer_dict, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        answer_dict = {}

    # 打印解析后的字典
    print(answer_dict)

if __name__=="__main__":
    ask()