import sys
import re
def ecrire_fichier(nom_fichier: str, contenu: list, encoding: str = 'UTF-16'):
   with open(nom_fichier, 'w', encoding=encoding) as f:
       f.write('\ufeff')
       f.writelines(contenu)

def ecrire3(meds: list, fichier: str, lettres: str = 'abcdeéfghijklmnopqrstuvwxyz'):
   total = 0
   with open(fichier, 'w', encoding='UTF-8') as f:
       for lettre in lettres:
           count = sum(1 for med in meds if med[0] == lettre)
           if count > 0:
               # Écrire les médicaments pour cette lettre
               for med in meds:
                   if med[0] == lettre:
                       f.write(med)
               f.write('-'*100 + '\n')
               f.write(f'total de {lettre}: {count}\n')
               f.write('-'*100 + '\n')
               total += count
       f.write(f'le nombre total de médicaments: {total}\n')
   return total


if len(sys.argv) < 2:
    print('insuffisant')
else:
    mots_exclus = {'mdz', 'hémoglobine', 'kt', 'le', 'b1', 'soit', 'sous', 
               'urée', 'mille', 'eau', 'virus', 'jusqu', 'puis','100','50'}
    listeEXT=[]
    lettres='abcdeéfghijklmnopqrstuvwxyz'
    f1 = open(str(sys.argv[1]), 'r', encoding='UTF-8')
    x=f1.readlines()
    for i in x:
        reg = re.search(r'^(?!\d)[-*Ø]?\s?(\w+)\s?:?\s?(\d+|,|\d+.\d)+\s?:?(\s(mg\s|MG|UI|ml|mcg|amp|iu|flacon|g|sachet|un\s|1/j|/j)(.+|\n)|(g|/j)\n|(mg)\s.+)', i, re.I)
        if reg :
                        mot = reg.group(1).lower()
                        if mot not in mots_exclus:
                                listeEXT.append(f"{mot},.N+subst\n")
    for i in x:
        reg = re.search(r'vitamine [A-Za-z]*', i, re.IGNORECASE)
        if reg:
            listeEXT.append(f"{reg.group().lower()},.N+subst\n")
   
# Dédoublonner et trier la liste
listeEXT = sorted(set(listeEXT))

ecrire_fichier('subst_corpus.dic', listeEXT)
ecrire3(listeEXT, 'infos2.txt')

try:
   with open('subst.dic', 'r', encoding='utf-16') as f:
       ancien_dict = set(f.readlines())
except FileNotFoundError:
   ancien_dict = set()

# Trouver les nouveaux médicaments
md = [med for med in listeEXT if med not in ancien_dict]
ecrire3(md, 'infos3.txt')
#fin
listeEXT = sorted(set(listeEXT) | ancien_dict)
ecrire_fichier('subst.dic', listeEXT)
print('files created.')
