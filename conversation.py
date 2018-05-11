#!/usr/bin/python

import csv
import re

# function definitions

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
    for i in range(1,len(temp)-1):
        if temp[i]!=newlist[-1]: newlist.append(temp[i])
    return newlist
    

# selecting budget
def budget(aaa):
    temp=aaa
    res=[0,0]
    
    if (temp.find('around')!=-1 or temp.find('approximately')!=-1 or temp.find('app.')!=-1 or temp.find('average')!=-1):
        res[0]='average'
    else:
        res[0]='max'
    
    temp=temp.replace("-"," ")
    temp=temp.replace("$"," ")
    temp=temp.split()
    
    temp2=[]
    for part in temp:
        if is_number(part): temp2.append(float(part))
    
    if len(temp2)==0:
        res[0]='error'
    elif len(temp2)==1:
        res[1]=temp2[0]
    elif len(temp2)==2:
        if temp2[1]<temp2[0]: temp2[0],temp2[1]=temp2[1],temp2[0]
        res=temp2
    else:
        res[0]='error'
    return res


# selecting brand
def select_brand(thiscategory,categories,brands,aaa=False):
    # brands for this type of products
    ind=indices(categories,thiscategory)
    brand=[brands[i] for i in ind]
    
    # compact list of brands for this type of product
    brandcompact=remove_duplicate(tuple(brand))
    
    # when the customer doesn't specify a brand
    if aaa==False:
        res=[1,ind]
        return res

    # when the customer specifies a brand
    # checking if the desired brand is offered
    temp=aaa
    temp=temp.lower()
    res=0
    for i in range(0,len(brand)):
        if (temp.find(brand[i].lower())!=-1):
            ind1=indices(brands,brand[i])
            ind2=indices(categories,thiscategory)
            ind=list(set(ind1).intersection(ind2))
            ind.sort()
            res=[0,ind]
            return res
            break
    res=[-1,ind]
    return res
    

# selecting the best option for a given brand preference and budget
def give_best_option(ind,brands,products,prices,desiredprice):
    selectedbrands=tuple([brands[i] for i in ind])
    selectedproducts=tuple([products[i] for i in ind])
    selectedprices=tuple([prices[i] for i in ind])
    
    # if the maximum price or a price range is given
    if (desiredprice[0]=='max' or is_number(desiredprice[0])==True):
        maxprice=desiredprice[1]
        ind0=0
        for i in range(1,len(selectedprices)):
            if (selectedprices[i]>selectedprices[ind0] and maxprice-selectedprices[i]>=0): ind0=i
        if selectedprices[i]>maxprice:
            desiredprice[0]='average'   # if there is no option <maxprice, look for the closest option >maxprice
            
    # if the average price is given
    if desiredprice[0]=='average':
        meanprice=desiredprice[1]
        pricediff=list(selectedprices)
        for i in range(0,len(selectedprices)):
            pricediff[i]=(selectedprices[i]-meanprice)**2
        ind0=pricediff.index(min(pricediff))
    
    res=[ind0,selectedbrands[ind0],selectedproducts[ind0],selectedprices[ind0]]
    return res


# gives offer
def give_offer(flag,offer):
    if (flag==1 or flag==0):    # brand not specified or specified and is in stock
        print(offer[1],' ',offer[2],' for ',offer[3],' euros/month would the best option for you. Would you like to order it?')
    elif (flag==-1):            # brand specified, but not in stock
        print("Unfortunately we don't carry that brand. As an alternative I would suggest ",offer[1],' ',offer[2],' for ',\
            offer[3]," euros/month. Would you like to order it?")
    
# end function definitions







# main program
# reading list of available products
pid=[]
allproductnames=[]
allbrands=[]
allproductcategories=[]
allpaymentplans=[]
with open('data.csv','r') as f:
    reader=csv.reader(f)
    for row in reader:
        pid.append(row[0])
        allproductnames.append(row[1])
        allbrands.append(row[2])
        allproductcategories.append(row[3])
        allpaymentplans.append(row[4])
        
del pid[0]
del allproductnames[0]
del allbrands[0]
del allproductcategories[0]
del allpaymentplans[0]

for i in range(0,len(allpaymentplans)): allpaymentplans[i]=float(allpaymentplans[i])

pid=tuple(pid)
allproductnames=tuple(allproductnames)
allbrands=tuple(allbrands)
allproductcategories=tuple(allproductcategories)
allpaymentplans=tuple(allpaymentplans)

pcat=allproductcategories
pcat=remove_duplicate(pcat)  # list of categories
keywords=[['computer','comp','laptop'],['drone'],['gaming','vr','virtual','reality'],['phone'],['home','alexa','cleaner'],['watch']]



# conversation
# selecting the category
print('''\nHello! What kind of product would you like?''')

while True:
    ans=input('---> ')
    exitscript(ans)
    ans=ans.lower()
    
    selectedcategory=0
    for i in range(0,len(pcat)):
        for j in range(0,len(keywords[i])):
            if (ans.find(keywords[i][j])!=-1):
                selectedcategory=pcat[i]
                break
        if (selectedcategory==pcat[i]): break
    if (selectedcategory==pcat[i]): break
    if selectedcategory==0:
        print('''Unfortunately we do not have that. We offer smartphones, drones, gaming and virtual reality equipment, laptops, smart watches and smart home devices. Please select one of those or type "stop" to leave the chat.''')

# checking the price range and brand preferences and selecting the appropriate product for each category

# selecting the product in the "Computing" category
if selectedcategory==pcat[0]:
    # finding the price and brand preferences
    ans=input('How much are you willing to spend?\n---> ')
    exitscript(ans)
    desiredprice=budget(ans)
    ans=input('Are you interested in any particular brand?\n---> ')
    exitscript(ans)
    if yes_no(ans):
        ans=input('Which brand would you like?\n---> ')
        exitscript(ans)
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands,ans)
    else:
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands)
    
    # finding the best product in the desired price range
    offer=give_best_option(selectedbrand[1],allbrands,allproductnames,allpaymentplans,desiredprice)
    give_offer(selectedbrand[0],offer)
    
# selecting the product in the "Drones" category
if selectedcategory==pcat[1]:
    # finding the price and brand preferences
    ans=input('How much are you willing to spend?\n---> ')
    exitscript(ans)
    desiredprice=budget(ans)
    ans=input('Are you interested in any particular brand?\n---> ')
    exitscript(ans)
    if yes_no(ans):
        ans=input('Which brand would you like?\n---> ')
        exitscript(ans)
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands,ans)
    else:
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands)
    
    # finding the best product in the desired price range
    offer=give_best_option(selectedbrand[1],allbrands,allproductnames,allpaymentplans,desiredprice)
    give_offer(selectedbrand[0],offer)

# selecting the product in the "Phones & Tablets" category
elif selectedcategory==pcat[3]:
    # finding the price and brand preferences
    ans=input('How much are you willing to spend?\n---> ')
    exitscript(ans)
    desiredprice=budget(ans)
    ans=input('Are you interested in any particular brand?\n---> ')
    exitscript(ans)
    if yes_no(ans):
        ans=input('Which brand would you like?\n---> ')
        exitscript(ans)
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands,ans)
    else:
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands)
    
    # finding the best product in the desired price range
    offer=give_best_option(selectedbrand[1],allbrands,allproductnames,allpaymentplans,desiredprice)
    give_offer(selectedbrand[0],offer)

# selecting the product in the "Wearables" category
elif selectedcategory==pcat[5]:
    # finding the price and brand preferences
    ans=input('How much are you willing to spend?\n---> ')
    exitscript(ans)
    desiredprice=budget(ans)
    ans=input('Are you interested in any particular brand?\n---> ')
    exitscript(ans)
    if yes_no(ans):
        ans=input('Which brand would you like?\n---> ')
        exitscript(ans)
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands,ans)
    else:
        selectedbrand=select_brand(selectedcategory,allproductcategories,allbrands)
    
    # finding the best product in the desired price range
    offer=give_best_option(selectedbrand[1],allbrands,allproductnames,allpaymentplans,desiredprice)
    give_offer(selectedbrand[0],offer)
        
    
    
