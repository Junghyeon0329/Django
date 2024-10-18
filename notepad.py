	# phone_number = serializers.SerializerMethodField()
	# name = serializers.SerializerMethodField()

	# class Meta:
	# 	model = User
	# 	fields = [
	# 		"id",
	# 		"name",
	# 		"phone_number",
	# 		"employee_number"
	# 	]

	# # time : 6.19s ~ 7.13s
	# def get_phone_number(self, obj) -> str:
	# 	## phone_number = serializers.SerializerMethodField()의 변수명 규칙을 따릅니다.
	# 	res = requests.get(f"{inner_server_address}/users/{obj.email_id}")		
	# 	return res.json()["success"]["phone_number"]
	
	# def get_name(self, obj) -> str:
	# 	## name = serializers.SerializerMethodField()의 변수명 규칙을 따릅니다.
	# 	res = requests.get(f"{inner_server_address}/users/{obj.email_id}")
	# 	return res.json()["success"]["name"]	