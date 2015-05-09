# -*- coding: utf-8 -*-
__author__ = 'karan'
import nltk
import re
import sys
import csv
posEmo=[]
negEmo=[]
def main():
    dicton=[]
    print("Start");
    tweetData=open("test.csv","r")
    # getting the stop words
    data=tweetData.read().split('\n')
    for i in data:
        tweet1=i;
        # tweet=i.split(',')
        # tweet1=tweet[0]
        stopWords = open("english.txt","r");
        stop_word = stopWords.read().split();
        AllStopWrd = []
        for wd in stop_word:
            AllStopWrd.append(wd);
        #print("stop words-> ",AllStopWrd);

        # sample and also cleaning it
        #tweet1= """"Best day of my life"""
        #print("old tweet-> ",tweet1)
        tweet1 = tweet1.replace("'t","t")
        tweet1 = tweet1.replace("'s","")
        tweet1 = tweet1.lower()
        tweet1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet1).split())
        #print(tweet1);
        tw = tweet1.split()
        #print(tw)

        #tokenize
        sentences = nltk.word_tokenize(tweet1)
        #print("tokenized ->", sentences)

        #remove stop words
        Otweet = tw
        #for w in tw:
          #  if w not in AllStopWrd:
         #       Otweet.append(w);
        #print("sans stop word-> ",Otweet)


        emoWord=[]
        emoMeaning=[]

        # get taggers for neg/pos/inc/dec/inv words
        taggers ={}
        negWords = open("neg.txt","r");
        neg_word = negWords.read().split();
        #print("ned words-> ",neg_word)
        posWords = open("pos.txt","r");
        pos_word = posWords.read().split();
        #print("pos words-> ",pos_word)
        incrWords = open("incr.txt","r");
        inc_word = incrWords.read().split();
        #print("incr words-> ",inc_word)
        decrWords = open("decr.txt","r");
        dec_word = decrWords.read().split();
        #print("dec wrds-> ",dec_word)
        invWords = open("inverse.txt","r");
        inv_word = invWords.read().split('\n');
        #print("inverse words-> ",inv_word)
        emoticons = open("emoticon.txt","r");
        emoSent = emoticons.read().split("\n");
        for i in emoSent:
            emo=i.split(" ")
            emoWord.append(emo[0])
            emoMeaning.append(emo[1])
        for nw in neg_word:
            taggers.update({nw:'negative'});
        for pw in pos_word:
            taggers.update({pw:'positive'});
        for iw in inc_word:
            taggers.update({iw:'inc'});
        for dw in dec_word:
            taggers.update({dw:'dec'});
        for ivw in inv_word:
            taggers.update({ivw:'inv'});
       # print("tagger-> ",taggers)
       # print(taggers.get('little'))

        # get parts of speech
        posTagger = [nltk.pos_tag(Otweet)]
        #print("posTagger-> ",posTagger)
        dictTagger =[]
        for token in posTagger:
            tokentagger =[]
            #print("token--> ",token)
            for tok in token:
                tklist =[]
                tklist.append(tok[0])
                tklist.append(tok[1])
                #print(tok[0],tok[1])
                if tok[0] in neg_word:
                    tklist.append('negative')
                if tok[0] in pos_word:
                    tklist.append('positive')
                if tok[0] in inc_word:
                    tklist.append('inc')
                if tok[0] in dec_word:
                    tklist.append('dec')
                if tok[0] in inv_word:
                    tklist.append('inv')
                if tok[0] in emoWord:
                    emoMeaningString=emoMeaning.index(tok[0])
                    if (emoMeaningString=="rolleyes" or emoMeaningString=="lol" or emoMeaningString=="sad" or emoMeaningString=="confused" or emoMeaningString=="tongue" or emoMeaningString=="angry" or emoMeaningString=="question" or emoMeaningString=="cry" or emoMeaningString=="uneasy" or emoMeaningString=="facepalm"):
                        negEmo.append(tok[0])
                    elif (emoMeaningString=="lol" or emoMeaningString=="cool" or emoMeaningString=="smile" or emoMeaningString=="bigsmile" or emoMeaningString=="surprised" or emoMeaningString=="neutral" or emoMeaningString=="wink" or emoMeaningString=="exclaim" or emoMeaningString=="heart" or emoMeaningString=="martini" or emoMeaningString=="mindblown" or emoMeaningString=="star" or emoMeaningString=="blush"):
                        posEmo.append(tok[0])
                tokentagger.append(tklist)
            dictTagger.append(tokentagger)
        #print(dictTagger)
        Cleantweet =[]
        for w in dictTagger[0]:
            if w[0] not in AllStopWrd:
                Cleantweet.append(w)

        #print("clan tweet",Cleantweet)
        sum = count(Cleantweet,None,0)

        if len(posEmo) > len(negEmo):
                sum=sum+3
        elif len(negEmo) > len(posEmo):
                sum=sum-3
        elif len(negEmo) == len(posEmo):
                sum=sum+0
        #print(sum)
        if sum > 0:
            newsomthing = [tweet1,'positive',sum]
        elif sum < 0:
            newsomthing = [tweet1,'negative',sum]
        elif sum ==0:
            newsomthing = [tweet1,'neutral',sum]
        dicton.append(newsomthing)
    #print (dicton)
    file2 = open('myfile2.csv','wb')
    writer = csv.writer(file2)
    writer.writerows(dicton)
    file2.close()

def count(current,previous,sum):
    #print("counting")
    #print("current-> ",current)
    #print("prev-> ",previous)

    if len(current)==0:
        return sum
    else:
        first = current[0]
        #print("first->",first)
        wording = first[0]
        tag1 = first[1]
        tag2 = ''
        if len(first) == 3:
            tag2 = first[2]
        #print("word tag tag",wording,tag1,tag2)
        score =0
        if tag2 is 'positive' or tag2 is 'negative':
            #print("either")
            if ('JJ' in tag1) or ('VB' in tag1) or ('RB' in tag1):
                if tag2 is 'positive':
                    score =score+1
                    #print(score)
                else:
                    score = score-1
                    #print(score)
        if previous is not None:
            if 'inc' in previous:
                if score==0:
                    score +=2.0
                else:
                    score *= 2.0
            elif 'dec' in previous:
                if score==0:
                    score -=2.0
                else:
                    score /= 2.0
            elif 'inv' in previous:
                if score==0:
                    score +=-2.0
                else:
                    score *=-2.0
        return count(current[1:], first, sum + score)

main();