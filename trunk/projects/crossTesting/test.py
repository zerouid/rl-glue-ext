#!/usr/bin/env python
import subprocess,os,signal,time

totalTests=0
subprocess.call(["killall rl_glue"],shell=True)

def run_test(agent, env, experiment):
	global totalTests
	debug=False
	totalTests+=1
	#If there are errors, a time.sleep 1 here might help
	allSubProcesses=[]
	cmds = ["rl_glue &",agent,env]
	for cmd in cmds:
		if debug:
			print "\t\trunning: "+cmd
			thisProc=subprocess.Popen([cmd],shell=True)
			print "\t\t\tIt has PID="+str(thisProc.pid)
			allSubProcesses.append(thisProc)
		else:
			thisProc=subprocess.Popen([cmd],shell=True,stdout=open(os.devnull,"w"), stderr=open(os.devnull,"w"))
			allSubProcesses.append(thisProc)

	time.sleep(.35)
	if debug:
		print "\t\texperiment: "+experiment
		retcode = subprocess.call([experiment],shell=True)
	else:
		retcode = subprocess.call([experiment],shell=True,stdout=open(os.devnull,"w"), stderr=open(os.devnull,"w"))

	time.sleep(.5)
	for someSubProcess in allSubProcesses:
		if debug:
			print "Calling Kill on PID: "+str(someSubProcess.pid)
		os.kill(someSubProcess.pid, signal.SIGKILL)
		

	if retcode!= 0:
		print "\t\tNonzero return code: "+str(retcode)
		exit(1)
	return retcode
	
	
def run_combinations_of_test(agentList, envList, experimentList):
	totalErrors=0
	for agentLang in agentList:
		for envLang in envList:
			for experimentLang in experimentList:
				print "\tCombination: "+agentLang+"/"+envLang+"/"+experimentLang
			
				totalErrors+=run_test(agentList[agentLang],envList[envLang],experimentList[experimentLang])
	return totalErrors;
	
def run_all_tests(testsList):
	totalErrors=0
	for test in testsList:
		print "Running Suite: "+test
		[agentList, envList, experimentList] = testsList[test]
		totalErrors+=run_combinations_of_test(agentList,envList,experimentList)

	return totalErrors
	
#These dicts keep mapping from language --> agents of various types
test_1_agent={}
test_empty_agent={}
test_message_agent={}

#These dicts keep mapping from language --> environments of various types
test_1_environment={}
test_empty_environment={}
test_message_environment={}
test_seeds_environment={}

#These dicts keep mapping from language --> experiments of various types
test_sanity_experiment={}
test_1_experiment={}
test_empty_experiment={}
test_message_experiment={}
test_seeds_experiment={}
test_rl_episode_experiment={}

test_1_agent["C"]="../codecs/C/tests/test_1_agent &";
test_1_agent["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_1_Agent &";

test_empty_agent["C"]="../codecs/C/tests/test_empty_agent &";
test_empty_agent["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Empty_Agent &";

test_message_agent["C"]="../codecs/C/tests/test_message_agent &";
test_message_agent["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Message_Agent &";

test_1_environment["C"]="../codecs/C/tests/test_1_environment &";
test_1_environment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_1_Environment &";

test_empty_environment["C"]="../codecs/C/tests/test_empty_environment &";
test_empty_environment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Empty_Environment &";

test_message_environment["C"]="../codecs/C/tests/test_message_environment &";
test_message_environment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Message_Environment &";

test_seeds_environment["C"]="../codecs/C/tests/test_seeds_environment &";
test_seeds_environment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Seeds_Environment &";

#Experiment should not have & at the end
test_sanity_experiment["C"]="../codecs/C/tests/test_sanity_experiment";
test_sanity_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Sanity_Experiment &";

test_1_experiment["C"]="../codecs/C/tests/test_1_experiment";
test_1_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_1_Experiment &";

test_message_experiment["C"]="../codecs/C/tests/test_message_experiment";
test_message_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Message_Experiment &";

test_empty_experiment["C"]="../codecs/C/tests/test_empty_experiment";
test_empty_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Empty_Experiment &";

test_seeds_experiment["C"]="../codecs/C/tests/test_seeds_experiment";
test_seeds_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_Seeds_Experiment &";

test_rl_episode_experiment["C"]="../codecs/C/tests/test_rl_episode_experiment"
test_rl_episode_experiment["Java"]="java -Xmx128M -classpath ../codecs/Java/dist/JavaCodec.jar org.rlcommunity.rlglue.tests.Test_RL_Episode_Experiment &";

#Define the high level tests here... IE: Map actual test names/labels to which
#agent/env/experiment should be used
tests={}

tests["test_sanity"]=[test_1_agent,test_1_environment,test_sanity_experiment];
tests["test_1"]=[test_1_agent,test_1_environment,test_1_experiment];
tests["test_empty"] = [test_empty_agent,test_empty_environment,test_empty_experiment];
tests["test_message"] = [test_message_agent,test_message_environment,test_message_experiment];
tests["test_rl_episode"] = [test_1_agent,test_1_environment,test_rl_episode_experiment];
tests["test_seeds"] = [test_1_agent,test_seeds_environment,test_seeds_experiment];

print "Running Codec Test Suites"
totalErrors=run_all_tests(tests)
print "Total Errors = "+str(totalErrors)+" on a total of: "+str(totalTests)+" tests"

