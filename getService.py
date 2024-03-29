def add_prefix_and_capitalize(input_str):
        return "I" + input_str[0].upper() + input_str[1:]
def get_get_part(service):
        return "get" + service[0].upper() + service[1:]
def get_service_method(service):
    service = service[0].lower() + service[1:]
    jiekou = ''
    if service:
        if not service.endswith("Service"):
            service += "Service"
        jiekou = add_prefix_and_capitalize(service)
        get_part = get_get_part(service)
        return f'''
	private {jiekou} {service};
	public {jiekou} {get_part}() {{
		if ({service} == null) {{
			{service} = ({jiekou}) SpringBeanUtil.getBean("{service}");
		}}
		return {service};
	}}
	'''
    else:
        return ''
def get_service_method_easy(service):
    service = service[0].lower() + service[1:]
    jiekou = ''
    if service:
        if not service.endswith("Service"):
            service += "Service"
        jiekou = add_prefix_and_capitalize(service)
        return f'''
	    {jiekou} {service} = ({jiekou}) SpringBeanUtil.getBean("{service}");
	'''
    else:
        return ''

