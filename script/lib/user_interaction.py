def ask_loock_root(prompt='Do you want to lock the root account ? (Y/n): '):
	return True if input(prompt) == 'Y' else False

def ask_num_hashing_rounds(prompt="Do you want to increase number of hashing round ? (65536 rounds) ? (Y/n): "):
	return True if input(prompt) == 'Y' else False
