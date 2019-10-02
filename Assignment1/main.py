from nltk.parse import CoreNLPParser
from nltk.tree import Tree
import re
from input_sentence import *

count=0

def traverse_tree(tree):
    global count
    leaf=tree.leaves()
    if len(leaf)==1:
        if tree.height()==2 and tree.label()!='.':
            count=count+1
            tree[0]=tree[0]+' - '+str(count)
    for subtree in tree:
        if type(subtree) == Tree:
            traverse_tree(subtree)
    return tree

def find_head(phrase):
    pos_tags=[]
    alltags=[]
    p=0
    leaf=1
    for i in phrase:
        if len(i)>1:
            leaf=0
    if leaf:
        for j in precedence_list:
            if p==1:
                break
            for word,pos in phrase.pos():        
                noun=re.match(j,pos)
                if noun and noun[0]:
                    return word
                    p=1
                    break
    else:
        for j in precedence_list:
            for subtree in phrase:
                pos=subtree.label().split()[0]
                noun=re.match(j,pos)
                if noun and noun[0]:
                    if len(subtree.label().split())>1:
                        return ' '.join(subtree.label().split()[1:])
                    else:
                        for word,pos in subtree.pos():
                            return word

def dep_tree(tree):
    global temp
    for subtree in tree:
        if type(subtree) == Tree:
            dep_tree(subtree)
    if len(tree)==1 and tree.height()>2 and len(tree.leaves())==1:
        leaf=tree.leaves()
        templabel=tree.label()
        newlabel=templabel+ ' ' + leaf[0]
        tree.set_label(newlabel)
    if len(tree)!=len(temp):
        leaf=tree.leaves()
        if len(leaf)>1:
            head=find_head(tree)
            if not head:
                raise Exception('There are certain phrases for which I cannot find the heads as I do not have all the rules.  Please add rules and try again')

            templabel=tree.label()
            newlabel=templabel+' '+head
            tree.set_label(newlabel)
        elif len(leaf)==1:
            templabel=tree.label()
            newlabel=templabel+ ' ' + leaf[0]
            tree.set_label(newlabel)
    else:
        return tree
    
def dep_list(tree,deplist):
    global temp
    global treehead
    for subtree in tree:
        if type(subtree) == Tree:
            dep_list(subtree,deplist)
    children=tree.leaves()
    if tree.height()>2:
        if len(children)!=len(temp.leaves()):
            for j in children:
                if j!=' '.join(tree.label().split()[1:]) and (j not in [i[1] for i in deplist]):
                    deplist.append([' '.join(tree.label().split()[1:]),j])
    return deplist

def sorting(elem):
    return elem[1].split()[2]

parser = CoreNLPParser(url='http://localhost:9000')
#Read the sentence and form the parse tree
parser_output_splitted=parser.parse(sentence.split())

for j in parser_output_splitted:
    temp=j
    
#Part 1
parser_output=traverse_tree(temp)
print(parser_output)

#Part 2
precedence_list=['VP','VB','VBG','VBZ',r'V*','NP','NN',r'N*','ADVP','JJ','P','RB','PRP$','PRP']
deptree=dep_tree(parser_output)
print(deptree)

#Part 3
for subtree in deptree:
    treehead=subtree.label()
deplist=[]
deplist=dep_list(deptree,deplist)
deplist.append(['ROOT - 0',' '.join(treehead.split()[1:])])
print(deplist)

#Part 4
deplist=sorted(deplist,key= sorting)
print(deplist)