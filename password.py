import requests
import hashlib
import sys

def send_request(first5_char):
	url = 'https://api.pwnedpasswords.com/range/' + first5_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Invalid status code {res.status_code}')
	else:
		return res

def leak_password_count(hashes,hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h,count in hashes:
		if h == hash_to_check:
			return count
	return 0

def check_pwned(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char,tail = sha1password[:5],sha1password[5:]

	response = send_request(first5_char)
	return leak_password_count(response, tail)

def main(args):
	for p in args:
		count = check_pwned(p)
		if count:
			print(f'Password: {p} was leaked {count} times.')
		else:
			print('Congrats! Your password is safe!')

main(sys.argv[1:])