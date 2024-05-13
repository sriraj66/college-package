import logging

logger = logging.getLogger(__name__)


def update_student_credit(sender, instance, **kwargs):
    check = instance.check_credit()

    if check is False:
        logger.warning("No Credit Left")
        return 

    balance = instance.balance_credit()
    
    usage = instance.calculate_credit()
    instance.credit_used = usage 
    new_balance =  instance.balance_credit()
    credit_burn = balance - new_balance
    
    if credit_burn > 0:
        instance.college.c_credit += credit_burn 
        instance.college.save()
        instance.save()
        logger.info("Done")
        print(balance,new_balance, usage, check,credit_burn)
    
        

def update_college_credit(sender, instance, **kwargs):
    try:
        
        instance.student_credit = instance.CPS()
    except Exception as e:
        print(e)