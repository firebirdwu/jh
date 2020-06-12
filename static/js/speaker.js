$(document).ready(function(){
    $('#bank_code').blur(function(){
        var bank_code=$(this).val();
            if(bank_code){
                console.log(bank_code);
                $.ajax({
                    url:"{{url_for('task.get_bankname')}}",
                    dataType:"json",
                    async:true,
                    type:'GET',
                    data:{'bankcode':bank_code},
                    success:function(data){
                       var bankname=data['bankname'];
                       console.log(bankname);
                       $('#bank_information').val(bankname);
                    }
                });
            };
    });
    $('#bank_code').blur(function(){
        var bank_code=$(this).val();
            if(bank_code){
                console.log(bank_code);
                $.ajax({
                    url:"{{url_for('task.get_bankname')}}",
                    dataType:"json",
                    async:true,
                    type:'GET',
                    data:{'bankcode':bank_code},
                    success:function(data){
                       var bankname=data['bankname'];
                       console.log(bankname);
                       $('#bank_information').val(bankname);
                    }
                });
            };
    });
});