$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/AreaInfo/update/" + $("#areaInfo_areaId_modify").val(),
		type : "get",
		data : {
			//areaId : $("#areaInfo_areaId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (areaInfo, response, status) {
			$.messager.progress("close");
			if (areaInfo) { 
				$("#areaInfo_areaId_modify").val(areaInfo.areaId);
				$("#areaInfo_areaId_modify").validatebox({
					required : true,
					missingMessage : "请输入区域id",
					editable: false
				});
				$("#areaInfo_areaName_modify").val(areaInfo.areaName);
				$("#areaInfo_areaName_modify").validatebox({
					required : true,
					missingMessage : "请输入区域名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#areaInfoModifyButton").click(function(){ 
		if ($("#areaInfoModifyForm").form("validate")) {
			$("#areaInfoModifyForm").form({
			    url:"AreaInfo/update/" + $("#areaInfo_areaId_modify").val(),
			    onSubmit: function(){
					if($("#areaInfoEditForm").form("validate"))  {
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
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#areaInfoModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
