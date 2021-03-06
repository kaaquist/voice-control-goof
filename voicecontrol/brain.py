from ttsstt import Conversation
import importlib

class Brain(object):
	def __init__(self, conversation, modules = []):
		self.conversation = conversation
		self.modules = []
		
		package_prefix = '.'.join(__name__.split('.')[:-1] + ['modules']) + '.'
		for module in modules:
			try:
				temp = importlib.import_module(package_prefix + module)
				if hasattr(temp,'valid_input') and hasattr(temp,'process_input'):
					self.modules.append(temp)
			except Exception as e:
				print 'Failed to load module', module, '(', repr(e),')'


	def process(self, text):
		reply = None
		processed = False

		# text from STT does not have any punctuation
		words = text.lower().split(' ') 

		for module in self.modules:
			if module.valid_input(self.conversation, words):
				(processed,reply) = module.process_input(self.conversation, words)
				break

		return (processed,reply)