#リストを定義する，リストを並び変える，for文を組む，ifで分ける，記録する，→最終的には，記録メモをクラスとして定義しよう
#自分から自分へを消す，a→bからb→aを引く
from collections import defaultdict

pay = [100, 30, 50, 0, 70, 130]
get = [10, 50, 130, 50, 20, 120]

name = ['a','b','c','d','e','f']

paymemo = []

net = []

#差額を計算する
for i in name:
    s = name.index(i)

    net.append(pay[s]-get[s]) 

#リスト内の要素内に，(0を含まない)異符号を含むときにのみtrueを返す関数
def same_sign(lst):
    pos = any(x>0 for x in lst)
    neg = any(x<0 for x in lst)
    return pos and neg

upnet = net[:]

#upnetを更新し続けながら，最大値+最小値で分配を繰り返す
while same_sign(upnet):
    maxim = max(upnet)
    minim = min(upnet)
    maxim_ind = upnet.index(maxim)
    minim_ind = upnet.index(minim)

    x = maxim+minim

    if x >= 0:
        print(f"{name[maxim_ind]}が{name[minim_ind]}に{-minim}払う")

        payer = name[maxim_ind]
        getter = name[minim_ind]
        amount = -minim

        paymemo.append((payer,getter,amount))

        upnet[maxim_ind] = x
        upnet[minim_ind] = 0
    else:
        print(f"{name[maxim_ind]}が{name[minim_ind]}に{maxim}払う")

        payer = name[maxim_ind]
        getter = name[minim_ind]
        amount = maxim

        paymemo.append((payer,getter,amount))
        upnet[maxim_ind] = 0
        upnet[minim_ind] = x


#(payer,getter,amount)のリスト
print(paymemo) 

#(payer,getter,amount)のリストを{(payer,getter):amount}と辞書型化
netdict = defaultdict(int)

for payer, getter, amount in paymemo:
    netdict[(payer,getter)] += amount

result = defaultdict(int)
processed = set()

#payer→getter,getter→payerの相殺を行う
for ((p,g), a) in netdict.items(): 
    if (p,g) in processed or (g,p) in processed:     #(p,g) in processedはなくてもいい
        continue
    if (g,p) in netdict:
        if netdict[(p,g)] >= netdict[(g,p)]:
            result[(p,g)] += netdict[(p,g)]-netdict[(g,p)]
        else:
            result[(g,p)] += netdict[(g,p)]-netdict[(p,g)]
    else:
        result[(p,g)] += a
    
    processed.add((p,g))

#相殺後にamount==0を削除(辞書をループしている最中にその辞書の削除・追加をしてはならないため，keyのリストto_deleteを定義して，それろ共通の元を持つresult[key]を削除)
to_delete = []

for ((p,g), a) in result.items():
    if a == 0:
        to_delete.append((p,g))
    else:
        pass

for (p,g) in to_delete:
    del result[(p,g)]

#結果の出力
for (p, g), a in sorted(result.items()):
    print(f"{p} が {g} に {a} 円払う")

