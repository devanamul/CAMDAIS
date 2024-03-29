from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import institute, systemAdmin, student, classes, test, currentInstituteTest, history
from datetime import datetime, timedelta
import random


def comments(name, value):
	# math anxrity
	value = float(value)
	if name == "Mathematical Anxiety":
		if value < 15:
			return "Do not have visible sign of nervousness or tension. This is very good and may be because of good preparation and positive disposition about Mathematics."
		elif value <35:
			return "Exhibit moderate level of nervousness which is healthy to keep a student focused and attentive."
		else:
			return "Exhibit a severe and unhealthy level of nervousness or tension which sometimes stem from very poor preparation/huge lack of basic knowledge/ tremendous pressure doing good which is not justified."
	# past exp
	elif name == "Past Experience":
		if value < 30:
			return "Seems to have pleasant learning experience and feels no discomfort towards Mathematical learning."
		elif value >=30 and value <= 45:
			return "Have good past experience in math learning"
		elif value < 60:
			return "Somewhat discontent about Mathematical learning that may be stemmed from lack of proper guidance and lack of practice."
		else:
			return "Has high level of discomfort towards Mathematical learning that stemmed either from unpleasant past experience or from poor teaching methodology and negative life experience associated with learning mathematics."
	# Working Memory
	
	# Numerical Skill
	elif name == "Numerical Skill":
		if value < 65:
			return "Very poor! Do not have required basic knowledge in mathematical operations."
		elif value >= 65 and value < 80:
			return "Satisfactory! Have basic knowledge in mathematical operations but have lacking in composite manipulation."
		elif value >=80 and value <= 90:
			return "Good! Indicates that the test taker possesses fairly good ability to solve basic arithmetic operations and perform estimates."
		else:
			return "Excellent! Indicates that the test taker possesses higher ability to solve basic arithmetic operations and perform estimates."

	# Learning Habit
	elif name == "Learning Habit":
		if value < 30:
			return "Very confident and has positive disposition towards learning Math."
		elif value < 45:
			return "Has positive attitude and good study habits."
		elif value <=60:
			return "Has lack of confidence and developed somewhat negative attitude"
		else:
			return "Has wrong perceptions and negative attitude towards learning mathematics."
	
	# Arithmetic
	elif name == "Arithmetic":
		if value < 55:
			return "Very poor! Do not have required basic knowledge in mathematical operations."
		elif value >=55 and value <= 70:
			return "Satisfactory! Have basic knowledge in mathematical operations but seems to have difficulties in statement and combined operational problems."
		elif value <= 85:
			return "Good! Have required basic knowledge and problem-solving skills."
		else:
			return "Excellent! Have solid basic knowledge in mathematical operations and strong manipulative skills."

	# Algebra
	elif name == "Algebra":
		if value < 55:
			return "Very poor! Have basic problem in definition, algebraic terminology, and manipulation."
		elif value >=55 and value <= 70:
			return "Satisfactory! Understands the basic concepts but have problems in carrying out instructions and algebraic manipulation."
		elif value <= 85:
			return "Good Performance! Have required basic knowledge and problem-solving skills."
		else:
			return "Excellent performance! Have strong basic knowledge in algebra."

	# Geometry
	elif name == "Geometry":
		if value < 55:
			return "Very poor! Have basic problem in geometrical literacy and application."
		elif value >=55 and value <= 70:
			return "Satisfactory! Have fair knowledge in geometry but have problems in applying them in solving problems."
		elif value <= 85:
			return "Good Performance: Understands and can use geometrical concepts to solve problems."
		else:
			return "Excellent performance! Have strong and deeper knowledge in geometry."

	# IQ
	elif name == "IQ":
		if value < 35:
			return "Extremely Low."
		elif value < 50:
			return "Below Average"
		elif value <70:
			return "Average"
		elif value <85:
			return "Above Average"
		else:
			return "Superior"
def home(request):
	return render(request, "CAMDAIS/home.html")

def dashboard(request):
	userType = None;
	u = request.user
	is_admin = systemAdmin.objects.filter(author=u)
	is_student = student.objects.filter(author=u)
	my_institute = None
	if is_admin.exists():
		userType = 'admin'
		print(userType)
		is_admin = systemAdmin.objects.get(author=u)
		my_institute = institute.objects.get(id=is_admin.institute.id)
	elif is_student.exists():
		userType = 'student'
		is_student = student.objects.get(author=u)
		my_institute = institute.objects.get(id=is_student.institute.id)
	print(u.first_name, userType)
	return render(request, "CAMDAIS/dashboard.html", {"user": u, 'userType': userType, 'my_institute':  my_institute})

def signin(request):
	if request.method == 'GET':
		return render(request, 'CAMDAIS/login.html')
	elif request.method == 'POST' and 'login' in request.POST:
		u = request.POST.get('username')
		p = request.POST.get('pass')
		user = authenticate(username=u, password=p)
		if user is None:
			return render(request, 'CAMDAIS/login.html')
		else:
			login(request, user)
			if user.is_superuser:
				return redirect('SuperUser')
			else:
				return redirect('Dashboard')
			
	elif request.method == 'POST' and 'SignUp' in request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		
		
		try:
			create_user = User.objects.create_user(
				username=username,
				email=email,
				first_name=first_name,
				last_name=last_name,
				password=password
				)
		except ValueError as e:
			error_message = str(e)
			return render(request, "CAMDAIS/login.html", {'error_message': error_message})
		
		create_user.save()
		messages.success(request, 'Successfully registered!')
		return redirect('SignIn')

def insttuteForm(request):
	if request.method == 'GET':
		return render(request, 'CAMDAIS/adminForm.html')
	elif request.method == 'POST':
		u = request.user
		name = request.POST.get('instituteName')
		instituteType = request.POST.get('InstituteType')
		current_institutes = institute.objects.filter(name = name)
		if current_institutes is  None:
			new_institute = institute(name=name, status = 0, instituteType=instituteType)
			new_institute.save()
			new_systemAdmin = systemAdmin(institute = new_institute, author = u, status = 0)
			new_systemAdmin.save()

			if new_institute.id and new_systemAdmin.id:
				print("Ok")
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/adminForm.html', {'message': "something is wrong, try again"})
		else:
			return render(request, 'CAMDAIS/adminForm.html', {'message': "Institute already exists, Enter valid institute name"})

def studentForm(request):
	u = request.user
	current_institutes = institute.objects.all()
	if request.method == 'GET':
		return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes})
	elif request.method == 'POST':
		institute_id = request.POST.get('Institute')
		level_str = request.POST.get('level')
		level = int(level_str)
		if 3 > level or level > 10:
			return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes, 'message': "this class is not exist, please enter a valid class number (3-10)"})
		else:
			my_institute = institute.objects.get(id = institute_id)
			new_student = student(author = u, level = level, status = 0, institute = my_institute)
			new_student.save()

			if new_student.id:
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes, 'message': "something is wrong, try again"})

def insttutePage(request):
	if request.method == 'GET':
		userType = None;
		u = request.user
		is_admin = systemAdmin.objects.filter(author=u)
		is_student = student.objects.filter(author=u)
		my_institute = None
		if is_admin.exists():
			userType = 'admin'
			print(userType)
			is_admin = systemAdmin.objects.get(author=u)
			my_institute = institute.objects.get(id=is_admin.institute.id)
		elif is_student.exists():
			userType = 'student'
			is_student = student.objects.get(author=u)
			my_institute = institute.objects.get(id=is_student.institute.id)
		return render(request, 'CAMDAIS/institutePage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute})

def studentPage(request):
	if request.method == 'GET':
		userType = None;
		u = request.user
		is_admin = systemAdmin.objects.filter(author=u)
		is_student = student.objects.filter(author=u)
		my_institute = None
		if is_admin.exists():
			userType = 'admin'
			print(userType)
			is_admin = systemAdmin.objects.get(author=u)
			my_institute = institute.objects.get(id=is_admin.institute.id)
		elif is_student.exists():
			userType = 'student'
			is_student = student.objects.get(author=u)
			my_institute = institute.objects.get(id=is_student.institute.id)
		return render(request, 'CAMDAIS/studentPage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute})

def attempt(request):
	u = request.user
	is_student = student.objects.get(author=u)
	my_institute = institute.objects.get(id=is_student.institute.id)
	if request.method == 'GET':
		userType = None;
		userType = 'student'
		print('level-', is_student.id, ' institute', my_institute.id)
		classN = classes.objects.get(Level=is_student.level)
		my_history = history.objects.filter(examinee = u, test_type = 0)
		if my_history.exists():
			return render(request, 'CAMDAIS/studentPage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'message': "You have already appeared this test"})
		is_test_exist = currentInstituteTest.objects.filter(institute=my_institute, class_id = classN)
		if is_test_exist.exists():

			test_list = []

			print("my level -", is_student.level)
			for each in ['Maths_Anxiety_symptoms', 'Past_Experience', 'Working_Memory', 'Numerical_skill', 'Algebra', 'Geometry', 'Arithmetic', 'Learning_Habit', 'IQ']:
				if getattr(classN, each):
					if each == 'Maths_Anxiety_symptoms':
						each = 'Mathematical Anxiety'
					elif each == 'Past_Experience':
						each = 'Past Experience'
					elif each == 'Working_Memory':
						each = 'Working Memory'
					elif each == 'Numerical_skill':
						each = 'Numerical Skill'
					elif each == 'Learning_Habit':
						each = 'Learning Habit'
					test_list.append(each)
					print(each)
			# class_dict[f'class_{i}'] = {'level': i, 'test': true_count}

			mytest_dict = {}

			for each in test_list:
				# print(each)
				tests = test.objects.filter(name = each, class_id = classN)
				random_tests = random.sample(list(tests), 5)
				inner_dict = {}
				count = 0
				for i in random_tests:
					count += 1
					ans = [i.rightAns, i.ans2, i.ans3, i.ans4]
					random.shuffle(ans)
					# print(i.question, " ", ans)
					inner_dict[f'{str(count)+i.name}'] = {'question': i.question, 'ans1': ans[0], 'ans2': ans[1], 'ans3': ans[2], 'ans4': ans[3]}
					
				
				mytest_dict[f'{each}'] = {'exam': inner_dict}
			# for each, current_dict in mytest_dict.items():
			# 	print(each)
			# 	for each, exam in current_dict.items():
			# 		for each, inner_exam in exam.items():
			# 			print(inner_exam['question'])
				# print(current_dict['exam'])
			# for each in mytest_dict:
			# 	print(mytest_dict[each])
			# print("check-",mytest_dict)
			return render(request, 'CAMDAIS/question.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'mytest_dict': mytest_dict})
		else:
			# print("not setisfied")
			return render(request, 'CAMDAIS/studentPage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'message': "You don't have any test now"})

	elif request.method == 'POST':
		catgory = request.POST.getlist('each[]')
		questions = request.POST.getlist('question[]')
		# print(questions)
		answers = []
		# print(request.POST)
		i = 1
		total_questions_per_category = 5
		for each in catgory:
			answer_key = f'answer{each}_{i}{each}'
			if i == total_questions_per_category:
				i = 1
			else:
				i = i+1
			print(answer_key)
			answer = request.POST.get(answer_key)
			answers.append(answer)

		correct_answers_count = {}

		for each, question, answer in zip(catgory, questions, answers):
			curr_question = test.objects.filter(question=question, name=each).first()
			if curr_question.rightAns == answer:
				correct_answers_count[each] = correct_answers_count.get(each, 0) + 1
				# print(curr_question.rightAns, " ", "ans ", answer, " correct")
			# else:
				# print(curr_question.rightAns, " ", "ans ", answer, "not correct")

		  # Assuming 5 questions per category
		percentage_correct_answers = {}
		for each in catgory:
			count = correct_answers_count.get(each, 0)
			# print(count)
			percentage_correct = (count / total_questions_per_category) * 100
			if each == 'Mathematical Anxiety':
				each = 'Maths_Anxiety_symptoms'
			elif each == 'Past Experience':
				each = 'Past_Experience'
			elif each == 'Working Memory':
				each = 'Working_Memory'
			elif each == 'Numerical Skill':
				each = 'Numerical_skill'
			elif each == 'Learning Habit':
				each = 'Learning_Habit'
			percentage_correct_answers[each] = percentage_correct
		my_admin = systemAdmin.objects.get(institute = my_institute)
		newhistory = history(test_type = 0, examiner=my_admin.author, examinee = u, level = is_student.level, **percentage_correct_answers)
		newhistory.save()
		for each, percentage in percentage_correct_answers.items():
			print(f"{each}: {percentage}%")
		return redirect('Dashboard')

def makeTest(request):
	userType = None;
	u = request.user
	is_admin = systemAdmin.objects.filter(author=u)
	is_student = student.objects.filter(author=u)
	my_institute = None
	if is_admin.exists():
		userType = 'admin'
		is_admin = systemAdmin.objects.get(author=u)
		my_institute = institute.objects.get(id=is_admin.institute.id)
	elif is_student.exists():
		userType = 'student'
		is_student = student.objects.get(author=u)
		my_institute = institute.objects.get(id=is_student.institute.id)
	class_dict = {}
	for i in range(3, 11):
		key = "class " + str(i)
		# print(key)
		classN = classes.objects.get(Level=i)
		true_count = 0
		for each in ['Maths_Anxiety_symptoms', 'Past_Experience', 'Working_Memory', 'Numerical_skill', 'Algebra', 'Geometry', 'Arithmetic', 'Learning_Habit', 'IQ']:
			if getattr(classN, each):
				true_count += 1
		class_dict[f'class_{i}'] = {'level': i, 'test': true_count}
	if request.method == 'GET':
		
		# for key in class_dict:
		# 	current_class = class_dict[key]
		# 	print(current_class['level'] , " ",  current_class['test'])
		
		return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict})
	
	elif request.method == 'POST':
		# level_str = request.POST.get('level')
		level = request.POST.get('level')
		print('level - ',level)
		my_class = classes.objects.get(Level = level)
		instituteId = request.POST.get('instituteId')
		my_institute = institute.objects.get(id = instituteId)
		startDate = datetime.now()
		endDate = datetime.now() + timedelta(days=5)
		# print("start date ", startDate, " ", endDate)
		current_test = currentInstituteTest.objects.filter(institute = my_institute, class_id = my_class)
		print(current_test)
		if current_test.exists():
			return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict, 'message': "Already there is a running test for this class"})
		else:
			new_currentInstituteTest = currentInstituteTest(institute = my_institute, class_id = my_class, startDate = startDate, endDate = endDate)
			new_currentInstituteTest.save()
			if new_currentInstituteTest.id:
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict, 'message': "something is wrong, try again"})
			
def AppearedResult(request):
	u = request.user
	is_student = student.objects.get(author=u)
	my_institute = institute.objects.get(id=is_student.institute.id)
	userType = 'student'
	# here i have to work for general user, this comment will remined me
	my_history = history.objects.filter(examinee = u, test_type = 0)
	if my_history.exists():
		my_history = history.objects.get(examinee = u, test_type = 0)
		if my_history.id:
			print("seticfied")
			result_dict = {}
			for column, value in my_history.__dict__.items():
				# print('column-',column, ': ', value)
				if value != None and column in ['Maths_Anxiety_symptoms', 'Past_Experience', 'Working_Memory', 'Numerical_skill', 'Algebra', 'Geometry', 'Arithmetic', 'Learning_Habit', 'IQ']:
					if column == 'Maths_Anxiety_symptoms':
						column = 'Mathematical Anxiety'
						value = str(100-float(value))
					elif column == 'Past_Experience':
						column = 'Past Experience'
						value = str(100-float(value))
					elif column == 'Working_Memory':
						column = 'Working Memory'
					elif column == 'Numerical_skill':
						column = 'Numerical Skill'
					elif column == 'Learning_Habit':
						column = 'Learning Habit'
						value = str(100-float(value))

					comment = comments(column, value)
					result_dict[column] = f'{comment}({value}%)'
			return render(request, 'CAMDAIS/resultAppeared.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'result_dict': result_dict})
	else:
		print("not seticfied")
		return render(request, 'CAMDAIS/studentPage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'message': "You have not appeared any test yet"})

def SuperUser(request):
	return render(request, "CAMDAIS/superUser.html")

def signout(request):
	logout(request)
	return redirect('homepage')