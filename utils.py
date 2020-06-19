try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']



def check_id_data2(id):
    mul=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    checksum_id=['1','0','x','9','8','7','6','5','4','3','2']
    sum=0
    for i in range(0,17):
        sum = sum+int(id[i])*mul[i]
    sum %=11
    if(checksum_id[sum]==str(id[17])):
        
        return True
    else:
       
        return False

'''
check id
'''
def check_identify(id):
    
    n=str(id)
    n17=n[:16]
    is_err=(not (n17.isdigit())) or (not (n[17].isdigit()) and n[17] !='x')
    msg=''
    result=False
    if is_err:
        msg='身份证号含0-9,x意外字符'
        result=False
    else:
        if check_id_data2(id):
            result = True
            msg='身份证校验通过'
        else:
            result = False
            msg = '身份证未校验通过'
    return result,msg      