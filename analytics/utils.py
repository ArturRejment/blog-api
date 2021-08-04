
def get_client_ip(request):
	x_forword_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forword_for:
		ip = x_forword_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR', None)
	return ip