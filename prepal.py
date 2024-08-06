import streamlit as st
from openai import OpenAI

openai_api_key = 'openapi-key'
# OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'introduction_submitted' not in st.session_state:
    st.session_state.introduction_submitted = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = []
    # feedback_prompt = "이렇게 영업 직무에 신입으로 지원하고자 하는 사람의 자소서가 있어. 그리고 크라운제과의 성장을 언급하셨습니다. 이 회사가 다른 기업들과 비교하여 특별히 매력적이라고 느낀 이유는 무엇인가요? 멋있어어요 이런식으로 면접 질문과 그에 대한 답변이 주어질거야. 그러면 자소서를 바탕으로 질문에 대한 답변이 올바른지, 부족하거나 고쳐야 할 부분이 있다면 무엇이 있을지 적극적으로 피드백 해줬으면 좋겠어. 출력 형식을 예시를 들어주면 만약 답변이 부실할 경우에는 개선점 : ~~ 답변 예시: ~~ 이렇게 보여줬으면 좋겠고 좋은 답변을 했을 경우에도 어느 부분이 좋았는지 간단하게 설명해주면 좋을 것 같아. 여기서 출력시 주의사항은 알겠습니다. 피드백을 작성하겠습니다. 이런 텍스트 없이 그냥 깔끔하게 개선점 : ~~ 답변 예시: ~~ 이런 피드백에 관련된 텍스트들만 출력될 수 있게 해줘"


# 페이지 설정
st.set_page_config(page_title="AI 모의 면접 서비스", layout="wide")

# 헤더
st.title("AI 모의 면접 서비스")
st.write("실전 같은 면접 연습과 피드백을 제공합니다.")

# 자기소개서 제출
if not st.session_state.introduction_submitted:
    st.subheader("자기소개서 제출")
    introduction = st.text_area("자기소개서를 입력하세요", height=200)

    if st.button("제출"):
        if introduction:
            st.write("자기소개서가 제출되었습니다. 면접을 시작하세요.")
            st.session_state.introduction_submitted = True 
            # 자소서 + 명령 prompt
            system_prompt = "너는 지금부터 영업직 신입채용을 하는 면접관이야. 면접 질문 플랜과 예시를 보고 적절한 질문 만들어줘. 면접 질문 플랜 1. 아이스트 브레이킹 (Ice-breaking). 면접 시작 전 긴장을 풀어주고 지원자와 면접관 간의 라포를 형성하기 위한 간단한 질문들. 2. 자기소개 및 경력사항. 지원자의 배경, 교육, 경력을 파악하는 단계. 3. 동기 및 목표. 지원자가 왜 이 직무에 지원했는지, 그리고 앞으로의 목표가 무엇인지 이해하는 단계. 4. 직무 관련 기술 및 역량 평가. 영업 사원으로서 필요한 기술 및 역량을 평가하는 단계. 5. 문제 해결 능력. 예상치 못한 상황에서의 대처 능력을 평가하는 단계. 6. 문화 적합성. 지원자가 회사의 문화와 잘 맞는지 평가하는 단계. 7. 추가 질문 및 마무리. 지원자의 궁금증을 해소하고, 마지막으로 하고 싶은 말을 들어보는 단계. 그리고 사용자가 준 자소서를 보고 면접 질문 플랜에 맞춰서 자소서에서 질문하고 싶은 내용이 있다면 참고해서 질문하면 돼. 총 15번 이상 질문을 플랜에 맞춰서 진행하면 되고 사용자의 답변에 따라서 추가 질문할 것이 있다면 더 자세한 추가 질문으로 대화가 이어지도록 진행해도 돼. 질문 3번에 1번 정도는 사용자의 답변을 이용해서 면접자가 당황할 수도 있는 압박 질문도 넣어줬으면 좋겠어. 한번에 모든 질문을 하지말고 사용자의 답변에 따라서 하나씩 질문해줘이제 사용자가 자소서를 보내면 첫번째 질문을 시작해줘. '1. 아이스트 브레이킹 질문: ' 이런거는 쓰지말고 실제 면접관이 직접 말할 것 같은 텍스트만 보내줘."
            
            st.session_state.messages.append({"role": "system", "content": system_prompt})
            st.session_state.messages.append({"role": "user", "content": introduction})
            # 챗봇의 질문 처리
            if len(st.session_state.messages) == 2:
                # Generate a question from the chatbot
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

            # Stream the response to the chat using `st.write_stream`, then store it in session state.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            
            st.rerun()
        else:
            st.warning("자기소개서 제출 후 버튼을 눌러주세요")

else:
    introduction = st.text_area("자기소개서를 입력하세요", height=200)
    prompt = st.chat_input("질문에 답변하세요.")
    # 레이아웃 설정
    col1, col2 = st.columns(2)

    with col1:
        # 챗봇 대화 형식
        st.subheader("면접 챗봇과 대화하기")

        # 기존 채팅 메시지 표시
        for messages in st.session_state.messages[2:]:
            with st.chat_message(messages["role"]):
                st.markdown(messages["content"])
    
        # 사용자의 응답 입력
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # OpenAI API를 사용하여 응답 생성
            if st.session_state.messages:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                # 응답을 채팅에 스트리밍하고 세션 상태에 저장
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})   

            feedback_prompt = f"""
            자소서:
            {introduction}
            질문:
            {st.session_state.messages[-3]['content']}
            답변:
            {st.session_state.messages[-2]['content']}
            이렇게 영업 직무에 신입으로 지원하고자 하는 사람의 자소서가 있어.
            그리고 크라운제과의 성장을 언급하셨습니다.
            이 회사가 다른 기업들과 비교하여 특별히 매력적이라고 느낀 이유는 무엇인가요? 멋있어어요
            이런식으로 면접 질문과 그에 대한 답변이 주어질거야. 그러면 자소서를 바탕으로 질문에 대한 답변이 올바른지,
            부족하거나 고쳐야 할 부분이 있다면 무엇이 있을지 적극적으로 피드백 해줬으면 좋겠어.
            출력 형식을 예시를 들어주면 만약 답변이 부실할 경우에는 개선점 : ~~ 답변 예시: ~~ 이렇게 보여줬으면 좋겠고
            좋은 답변을 했을 경우에도 어느 부분이 좋았는지 간단하게 설명해주면 좋을 것 같아. 여기서 출력시 주의사항은 알겠습니다.
            피드백을 작성하겠습니다. 이런 텍스트 없이 그냥 깔끔하게 개선점 : ~~ 답변 예시: ~~ 이런 피드백에 관련된 텍스트들만 출력될 수 있게 해줘
            """
            feedback_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": feedback_prompt}
            ],
            # stream=True,
            )
            st.session_state.feedback.append(feedback_response.choices[0].message.content)

    with col2:  
        # 피드백 생성
        # feedback = "좋은 답변입니다. 하지만 좀 더 구체적인 예시를 들어주시면 좋겠습니다."
        
        st.subheader("피드백")
        if st.session_state.feedback:
            st.write(st.session_state.feedback[-1])
