function getData(){
        var username = $('#username').val();
        var password = $('#password').val();
        var name = $('#name').val();
        var message = JSON.stringify({
                "username": username,
                "password": password,
                "name":name
            });
        if (name=='')
        {
             return alert(JSON.stringify("Please check the required fields."));
        }
        if (username=='')
        {
             return alert(JSON.stringify("Please check the required fields."));
        }
        if (password=='')
        {
            return alert(JSON.stringify("Please check the required fields."));
        }
        $.ajax({
            url:'/users',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                $.ajax({
                        url:'/CrearUsuarios',
                        type:'POST',
                        contentType: 'application/json',
                        data : message,
                        dataType:'json',
                        success: function(response){
                            alert(JSON.stringify(response));
                        },
                        error: function(response){
                          if(response["status"]==401){
                                alert("Try again");
                            }else{
                                window.location.href = " http://127.0.0.1:5000/static/index.html";

                            }

                        }
                    });
            },
        });
    }