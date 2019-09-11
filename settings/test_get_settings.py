def get_token():
    with open('token.txt', 'r') as file:
        token, bot_name = file.readline().split(sep=';')
    return token.split(sep=' = ')[1]


if __name__ == '__main__':
    token = get_token()
    print(token)
