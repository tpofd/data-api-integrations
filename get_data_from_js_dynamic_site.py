'''
This is an example of getting data from dynamic js site with auth
You can also use this example to get data from API because it has the same algorithm
Look more documentation about how to take access to site API:

'''

def get_data_from_js_dynamic_site(login_url, email, password, header, main_link):

    '''
    :param login_url: url for auth api
    :param email: your site login
    :param password: your site password
    :param header: user-agent in api 
    :param main_link: your main get request 
    :return: result of get request 
    '''

    from requests_html import HTMLSession

    headers = {
        'user-agent': header
    }
    
    # you should check that there enough params to your login api 
    data = {
        'email': email,
        'password': password
    }

    session = HTMLSession()
    session.headers.update(headers)

    # login to our site
    response = session.post(login_url, data=data)

    result = session.get(main_link)

    # you can work with result of this get request like as api
    # example of json result result.json()['column']
    
    return result
