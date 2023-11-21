from user_agents import parse


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_user_agent(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    if ua_string:
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        browser = user_agent.browser
        os = user_agent.os
        device = user_agent.is_pc and 'PC' or user_agent.device.family

        return device, os.family, browser.family
    else:
        return 'Other', 'Other', 'Other'
