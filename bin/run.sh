#docker run -it \
#--rm \
#--cpus="1" \
#--memory="512m" \
#--memory-swap="1024m" \
#chatbot
uvicorn main:app --reload
