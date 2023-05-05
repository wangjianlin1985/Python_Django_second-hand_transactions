$(function () {
	//实例化商品描述编辑器
    tinyMCE.init({
        selector: "#product_productDesc",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
	$("#product_productName").validatebox({
		required : true, 
		missingMessage : '请输入商品名称',
	});

	$("#product_price").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入商品价格',
		invalidMessage : '商品价格输入不对',
	});

	$("#product_connectPerson").validatebox({
		required : true, 
		missingMessage : '请输入联系人',
	});

	$("#product_connectPhone").validatebox({
		required : true, 
		missingMessage : '请输入联系电话',
	});

	$("#product_addTime").datetimebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#productAddButton").click(function () {
		if(tinyMCE.editors['product_productDesc'].getContent() == "") {
			alert("请输入商品描述");
			return;
		}
		//验证表单 
		if(!$("#productAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#productAddForm").form({
			    url:"/Product/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#productAddForm").form("validate"))  { 
	                	$.messager.progress({
							text : "正在提交数据中...",
						}); 
	                	return true;
	                } else {
	                    return false;
	                }
			    },
			    success:function(data){
			    	$.messager.progress("close");
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#productAddForm").form("clear");
                        tinyMCE.editors['product_productDesc'].setContent("");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#productAddForm").submit();
		}
	});

	//单击清空按钮
	$("#productClearButton").click(function () { 
		//$("#productAddForm").form("clear"); 
		location.reload()
	});
});
