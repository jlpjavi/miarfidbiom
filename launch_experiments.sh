shopt -s nullglob

python Roc.py scoresA_clientes.txt scoresA_impostores.txt

sleep 1

`mv  ROC.png ROC_A.png`

python Roc.py scoresB_clientes.txt scoresB_impostores.txt

sleep 1

`mv  ./ROC.png ROC_B.png`


