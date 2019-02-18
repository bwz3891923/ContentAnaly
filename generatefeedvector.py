import feedparser
import re
import sys

def getwordcounts(url):
    d=feedparser.parse(url)
    title=d.feed['title']
    wc={}
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        words=getWords(e.title+' '+summary)
        for word in words:
          wc.setdefault(word,0)
          wc[word]+=1

    return title,wc
          
    


def getWords(html):
    txt=re.compile(r'<[^>]+>').sub('',html)
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word !='']

def main():
    wordcounts={}
    apcount={}
    with open('recorrect.txt','r') as file:
        feedlist=[line for line in file]
        for feedurl in feedlist:
            print("Excuting:",feedurl)
            title,wc=getwordcounts(feedurl)
            wordcounts.setdefault(title,{})
            wordcounts[title]=wc
            for word,count in wc.items():
                apcount.setdefault(word,0)
                if count>1:
                    apcount[word]+=1

    wordlist=[]
    for w,bc in apcount.items():
        frac=float(bc)/len(feedlist)
        if frac>0.1 and frac<0.5:wordlist.append(w)

    out=open('blogdata.txt','w')
    out.write('Blog')
    for word in wordlist: out.write('\t%s'%word)
    out.write('\n')
    for blog,wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc : out.write('\t%d'%wc[word])
            else: out.write('\t0')
        out.write('\n')

main()

        
