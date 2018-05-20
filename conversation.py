#!/usr/bin/python

import csv
import re

# function definitions

# some small helpful functions
# exit script
def exitscript(aaa):
    temp=aaa.lower()
    if (temp.find('quit')!=-1 or temp.find('stop')!=-1 or temp.find('exit')!=-1 or temp.find('bye')!=-1):
        print("Good bye!")
        quit()


# checks if string is a number (int or float)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    

# finds indices of occurances of b in the list a
def indices(a, b):
    return [i for (i, val) in enumerate(a) if val==b]


# for yes/no questions
def yes_no(aaa):
    temp=aaa.lower()
    if not(temp.find('y')!=-1 or temp.find('n')!=-1):
        temp=input("I don't understand. Please answer yes or no.\n---> ")
        temp=temp.lower()
    if (temp.find('y')!=-1): res=True
    elif (temp.find('n')!=-1): res=False
    return res


# removing duplicates from a list
def remove_duplicate(oldlist):
    temp=list(oldlist)
    temp.sort()
    newlist=[temp[0]]
    for i in range(1,len(temp)):
        if temp[i]!=newlist[-1]: newlist.append(temp[i])
    return newlist
    


# functions for selection of the product
# selecting a product by number from a printed list of products (needed by select_price)
def select_product_by_number(anssel,indtypebrandprice,allbrands,allproductnames,allpaymentplans):
    ans=anssel.lower()
    
    while True:
        ans=ans.split()
        
        selnum=[]
        for part in ans:
            if part.isdigit(): selnum.append(int(part))
        
        if (len(selnum)!=1 or selnum[0]>len(indtypebrandprice) or selnum[0]<1):
            ans=input('Please select only one number from the list or type "bye" to leave the chat!\n---> ')
            exitscript(ans)
        else:
            break
    print("Great! You selected ",allbrands[indtypebrandprice[selnum[0]-1]],\
        " ",allproductnames[indtypebrandprice[selnum[0]-1]],
        " for ",allpaymentplans[indtypebrandprice[selnum[0]-1]],\
        " euro/month. Please, proceed to checkout. Good bye!")


# selecting the product for given average price
def select_product_for_given_average_price(avprice,indtypebrand,indtype,allbrands,allproductnames,allpaymentplans):
    # prices for the selected product type and brand
    pricesforthistypebrand=list(allpaymentplans[i] for i in indtypebrand)
    pcb=tuple(remove_duplicate(pricesforthistypebrand))
    
    pricesforthistype=list(allpaymentplans[i] for i in indtype)
    pc=tuple(remove_duplicate(pricesforthistype))
    
    pricediff=list(pcb)
    for i in range(0,len(pricediff)): pricediff[i]=(pcb[i]-avprice)**2
    indbestprice=pricediff.index(min(pricediff))
    bestprice=pcb[indbestprice]
    indprice=indices(pricesforthistypebrand,bestprice)
    indtypebrandprice=list(indtypebrand[i] for i in indprice)
        
    if len(indtypebrandprice)==1:       # only one product with the suitable price
        print("The best product for you is ",allbrands[indtypebrandprice[0]]," ",\
            allproductnames[indtypebrandprice[0]],"for ",allpaymentplans[indtypebrandprice[0]],\
            "euros/month. Would you like to take it?")
        anssel=input("---> ")
        exitscript(anssel)
        if yes_no(anssel):
            print("Great! Please, procede to checkout. Good bye!")
        else:
            print("I'm sorry you don't like it. Good bye!")
        
    else:                               # more than one products with the suitable price
        print(len(indtypebrandprice)," products fit your requirements:")
        for i in range(0,len(indtypebrandprice)):
            print("%2d  %10s  %70s for %5.2f euros/month" % (i+1,allbrands[indtypebrandprice[i]],\
                allproductnames[indtypebrandprice[i]],allpaymentplans[indtypebrandprice[i]]))
        anssel=input('''Which of these products would you like? Please type the product number or "bye" to leave the chat .\n---> ''')
        exitscript(anssel)
        select_product_by_number(anssel,indtypebrandprice,allbrands,allproductnames,allpaymentplans)

# selecting the product for given maximum price or range
def select_product_for_given_range(indtypebrand,indtype,allbrands,allproductnames,allpaymentplans,pricerange):
    # prices for the selected product type and brand
    pricesforthistypebrand=list(allpaymentplans[i] for i in indtypebrand)
    pcb=tuple(remove_duplicate(pricesforthistypebrand))
    
    pricesforthistype=list(allpaymentplans[i] for i in indtype)
    pc=tuple(remove_duplicate(pricesforthistype))
    
    # finding the indices of suitable product for max price and for range
    if len(pricerange)==1:
        maxprice=pricerange[0]
        indtypebrandprice=list(indtypebrand[i] for i in range(0,len(indtypebrand)) if \
            allpaymentplans[indtypebrand[i]]<=maxprice)
        indtypeprice=list(indtype[i] for i in range(0,len(indtypebrand)) if \
            allpaymentplans[indtype[i]]<=maxprice)
    elif len(pricerange)==2:
        maxprice=pricerange[1]
        indtypebrandprice=list(indtypebrand[i] for i in range(0,len(indtypebrand)) if \
            (allpaymentplans[indtypebrand[i]]>=pricerange[0] and allpaymentplans[indtypebrand[i]]<=pricerange[1]))
        indtypeprice=list(indtype[i] for i in range(0,len(indtypebrand)) if \
            (allpaymentplans[indtype[i]]>=pricerange[0] and allpaymentplans[indtype[i]]<=pricerange[1]))
        
    if len(indtypebrandprice)<1:
        # no products from that brand in given price range
        if len(indtypeprice)<1:
            # no products from any brand in given price range
            ans1=input("""Unfortunately there are no products that fit your requirements. Would you like to see the cheapest available product?\n---> """)
            exitscript(ans1)
            if yes_no(ans1):
                # finding the cheapest brand product
                select_product_for_given_average_price(maxprice,indtypebrand,indtype,\
                    allbrands,allproductnames,allpaymentplans)
            else:
                # not able to find a ssuitable product
                print("""I'm sorry I couldn't help you find anything suitable. Good bye!""")
        else:
            # no products from given brand, but there are some from other brands
            ans2=input("""There are no suitable products for the brand you requested. Would you like to see other brands products in this price range?\n---> """)
            exitscript(ans2)
            if yes_no(ans2):
                # selecting a product from other brands
                for i in range(0,len(indtypeprice)):
                    print("%2d  %10s  %70s for %5.2f euros/month" % (i+1,allbrands[indtypeprice[i]],\
                        allproductnames[indtypeprice[i]],allpaymentplans[indtypeprice[i]]))
                print('''Would you like any of them? If yes, please type the product number. If not, I can also show you the cheapest ''',allbrands[indtypebrand[0]], " product.")
                ans3=input("---> ")
                exitscript(ans3)
                if ans3.isdigit():
                    select_product_by_number(ans3,indtypeprice,allbrands,allproductnames,allpaymentplans)
                else:
                    select_product_for_given_average_price(maxprice,indtypebrand,indtype,\
                        allbrands,allproductnames,allpaymentplans)
            else:
                # suggesting the cheapest brand product
                print("Would you like to see the cheapest ",allbrands[indtypebrand[0]]," product?")
                ans4=input("---> ")
                exitscript(ans4)
                if yes_no(ans4):
                    # finding the cheapest brand product
                    select_product_for_given_average_price(maxprice,indtypebrand,indtype,\
                        allbrands,allproductnames,allpaymentplans)
                else:
                    # not able to find a ssuitable product
                    print("""I'm sorry I couldn't help you find anything suitable. Good bye!""")
    else:
        # there are suitable products from given brand and in the given price range
        print("""Products suitable for your needs are:""")
        for i in range(0,len(indtypebrandprice)):
            print("%2d  %10s  %70s for %5.2f euros/month" % (i+1,allbrands[indtypebrandprice[i]],\
                allproductnames[indtypebrandprice[i]],allpaymentplans[indtypebrandprice[i]]))
        anssel=input('''Which of these products would you like? Please type the product number or "bye" to leave the chat .\n---> ''')
        exitscript(anssel)
        select_product_by_number(anssel,indtypebrandprice,allbrands,allproductnames,allpaymentplans)
        
        
# selecting product category and, if there are more different types of product in the category, select the type
# (only for Smart Home category)
def select_product_type(anstype,allproductcategories,allproductnames):
    cat=allproductcategories
    cat=remove_duplicate(cat)  # list of categories
    keywords=[['computer','comp','laptop'],['drone'],['gaming','vr','virtual','reality'],['phone'],\
        ['home','alexa','cleaner','vacuum','robot','coffee','maker','qbo','milk','foam'],['watch']]
    ans=anstype.lower()
    
    # selecting the category
    while True:    
        selectedcategory=0
        for i in range(0,len(cat)):
            for j in range(0,len(keywords[i])):
                if (ans.find(keywords[i][j])!=-1):
                    selectedcategory=cat[i]
                    break
            if (selectedcategory==cat[i]): break
        if (selectedcategory==cat[i]): break
        if selectedcategory==0:
            print('''Unfortunately we do not have that. We offer smartphones, drones, gaming and virtual reality equipment, laptops, smart watches and smart home devices. Please select one of those or type "bye" to leave the chat.''')
            ans=input('---> ')
            exitscript(ans)
            ans=ans.lower()
    
    # finding the indices of all products from this category
    indcategory=indices(allproductcategories,selectedcategory)
    
    # if the category is Smart Home, search for the specific product type
    if selectedcategory=='Smart Home':
        # smart home product types: alexa, coffee maker thing, robotic vacuum cleaner
        keywords_smarthome=[['alexa','digital','assistant','amazon','voice'],\
            ['coffee','maker','milk','foam','qbo'],\
                ['vacuum','cleaner','robot']]
        ind_smarthome=[[indcategory[0],indcategory[1]],[indcategory[2]],[indcategory[3],indcategory[4]]]
        while True:
            selectedtype=0
            for i in range(0,3):
                for j in range(0,len(keywords_smarthome[i])):
                    if (ans.find(keywords_smarthome[i][j])!=-1):
                        selectedtype=1
                        indtype=ind_smarthome[i]
                        break
                if (selectedtype!=0): break
            if (selectedtype!=0): break
            if (selectedtype==0):
                print('''In the Smart Home category we offer Alexa, QBO Milk Master and robotic vacuum cleaners. Please select one of those or type "bye" to leave the chat.''')
                ans=input('---> ')
                exitscript(ans)
                ans=ans.lower()
    else:
        indtype=indcategory
    
    res=[indtype,selectedcategory]
    return res


# selecting the brand
def select_brand(ansbrand,indtype,allbrands):
    brandsinthiscategory=list(allbrands[i] for i in indtype)
    bitc=remove_duplicate(brandsinthiscategory)
    ans=ansbrand.lower()
    
    if (ans=='no' or ans=='nope' or ans.find('whatever')!=-1 or ans.find('any')!=-1 or (ans.find('don')!=-1 \
        and ans.find('care')!=-1) or ans.find('all')!=-1):
        # if the answer is no, select all brands
        indtypebrand=indtype
        selectedbrand='all'
    else:
        # check if the answer is yes, if yes, ask for the brand
        if (ans=='yes' or ans=='yep'):
            ans=input('''Which brand would you like?\n---> ''')
            exitscript(ans)
            ans=ans.lower()
        
        # look for the brand
        while True:
            selectedbrand=0
            for i in range(0,len(bitc)):
                if (ans.find(bitc[i].lower())!=-1):
                    selectedbrand=bitc[i]
                    break
            if (selectedbrand!=0): break
            if (selectedbrand==0):
                print('''We carry brands ''',end='')
                for i in range(0,len(bitc)):
                    if (i==len(bitc)-1):
                        print(bitc[i],end='. ')
                    elif (i==len(bitc)-2):
                        print(bitc[i],end=' and ')
                    else:
                        print(bitc[i],end='. ')
                print('''Please select one of those, type "any" if you don't have any brand preferences or type "bye" to leave the chat.''')
                ans=input('---> ')
                exitscript(ans)
                ans=ans.lower()
                if (ans.find('any')!=-1):
                    selectedbrand='any'
                    indtypebrand=indtype
                    break
        if selectedbrand!='any':
            indbrand=indices(brandsinthiscategory,selectedbrand)
            indtypebrand=list(indtype[i] for i in indbrand)
    
    res=[indtypebrand,selectedbrand]
    return res


# selecting the payment plan
def select_price(ansprice,indtypebrand,indtype,allbrands,allproductnames,allpaymentplans):
    ans=ansprice.lower()
    
    # finding out whether the desired price is a maximum or average
    if (ans.find('around')!=-1 or ans.find('approximately')!=-1 or ans.find('average')!=-1): budget='average'
    elif (ans.find('max')!=-1 or ans.find('tops')!=-1 or ans.find('up to')!=-1): budget='max'
    else: budget='max'
    
    # finding the numbers and checking if the budget is a range or unlimited
    ans=ans.replace("-"," ")
    ans=ans.replace("$"," ")
    ans=ans.split()
    
    numbers=[]
    for part in ans:
        if is_number(part): numbers.append(float(part))
        
    if len(numbers)==0:
        budget='unlimited'
    elif len(numbers)==2:
        budget='range'

    # finding the best possible device
    if budget=='average':
        select_product_for_given_average_price(numbers[0],indtypebrand,indtype,\
            allbrands,allproductnames,allpaymentplans)
    
    elif (budget=='max' or budget=='range'):
        select_product_for_given_range(indtypebrand,indtype,\
            allbrands,allproductnames,allpaymentplans,numbers)
        
    elif budget=='unlimited':
        print("""Products that would fit your requirements are:""")
        for i in range(0,len(indtypebrand)):
            print("%2d  %10s  %70s for %5.2f euros/month" % (i+1,allbrands[indtypebrand[i]],\
                allproductnames[indtypebrand[i]],allpaymentplans[indtypebrand[i]]))
        anssel=input('''Which of these products would you like? Please type the product number or "bye" to leave the chat .\n---> ''')
        exitscript(anssel)
        select_product_by_number(anssel,indtypebrand,allbrands,allproductnames,allpaymentplans)
        
                    
    
# end function definitions







# main program
# reading list of available products
allproductid=[]
allproductnames=[]
allbrands=[]
allproductcategories=[]
allpaymentplans=[]
with open('data.csv','r') as f:
    reader=csv.reader(f)
    for row in reader:
        allproductid.append(row[0])
        allproductnames.append(row[1])
        allbrands.append(row[2])
        allproductcategories.append(row[3])
        allpaymentplans.append(row[4])
        
del allproductid[0]
del allproductnames[0]
del allbrands[0]
del allproductcategories[0]
del allpaymentplans[0]

for i in range(0,len(allpaymentplans)): allpaymentplans[i]=float(allpaymentplans[i])

allproductid=tuple(allproductid)
allproductnames=tuple(allproductnames)
allbrands=tuple(allbrands)
allproductcategories=tuple(allproductcategories)
allpaymentplans=tuple(allpaymentplans)




# conversation
anstype=input("Hello! What kind of product would you rent from us?\n---> ")
exitscript(anstype)
seltype=select_product_type(anstype,allproductcategories,allproductnames)
indtype=seltype[0]

ansbrand=input("Are you especially interested in any particular brand?\n---> ")
exitscript(ansbrand)
selbrand=select_brand(ansbrand,indtype,allbrands)
indtypebrand=selbrand[0]

ansprice=input("How much money are you willing to spend?\n---> ")
exitscript(ansprice)
selprice=select_price(ansprice,indtypebrand,indtype,allbrands,allproductnames,allpaymentplans)
