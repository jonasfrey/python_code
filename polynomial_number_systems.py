
# polynomials 
# dec: 243       =>       2        4        3
#                         2*10² +  4*10¹ +  3*10⁰     
#                         200   +  40    +  3        => 243
#
# bin: 11110011  =>       1        1        1        1        0        0        1        1    
#                         1*2⁷ +   1*2⁶ +   1*2⁵ +   1*2⁴ +   0*2³ +   0*2² +   1*2¹ +   1*2⁰
#                         128  +   64   +   32   +   16   +   0    +   0    +   2    +   1        => 243
# 
# hex: e3        =>       e(13)     3
#                         13*16¹ +  3*16⁰
#                         240    +  3        => 243
#
# sexagesimal:43 =>       4         3        
#                         4*60¹  +  3*60⁰
#                         240    +  3        => 243
# 
# tridecimal:159 =>       1         5        9
#                         1*13²  +  5*13¹  + 9*13⁰ 
#                         169    +  65     + 9        => 243
#                       
#            

# challenge , create a function which can convert numbers from and into different number systems !

def conver_number_from_to(base_from , base_to, value){
    if(base_to == 16):
        # a = 10
        # b = 11
        # c = 12
        #...
}