from client import get_data, delete_data, post_data, put_data

print(post_data(url="http://localhost:8888", text_message='hi', queue=1))
print(get_data("http://localhost:8888", queue=1))
print(post_data(url="http://localhost:8888", text_message='hi', queue=1))
print(delete_data("http://localhost:8888", queue=1))
print(get_data("http://localhost:8888", queue=1))
print(put_data("http://localhost:8888", text_message='you', queue=1))
