# !/bin/bash

echo "===================RULE INTERPRETER TEST======================"
sleep 1
cd rule_interpreter/unit_tests/
python3 rule_interpreter_test.py
echo "=============================================================="

echo "===================RULE_ENACTOR_TESTS======================"
sleep 1
cd ../../game_engine/
python3 rule_enactor_unit_tests.py
echo "=============================================================="

cd ..
echo "===================CLIENT TESTS======================"
rm -f test.db
sleep 1
python3 server.py testkey test/test.conf &
cd test
sleep 1
SERVER_PID=$!
echo 'SERVER_PID is '
echo $SERVER_PID
python3 test_client.py
kill -SIGTERM $SERVER_PID
echo "=============================================================="
echo "===================USER TESTS======================"
sleep 1
python3 test_user.py
echo "=============================================================="
echo "===================ACCOUNT MANAGER TESTS======================"
sleep 1
python3 test_acccount_manager.py
echo "=============================================================="