$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/OldLevel/update/" + $("#oldLevel_levelId_modify").val(),
		type : "get",
		data : {
			//levelId : $("#oldLevel_levelId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (oldLevel, response, status) {
			$.messager.progress("close");
			if (oldLevel) { 
				$("#oldLevel_levelId_modify").val(oldLevel.levelId);
				$("#oldLevel_levelId_modify").validatebox({
					required : true,
					missingMessage : "请输入新旧程度id",
					editable: false
				});
				$("#oldLevel_levelName_modify").val(oldLevel.levelName);
				$("#oldLevel_levelName_modify").validatebox({
					required : true,
					missingMessage : "请输入新旧程度名称",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#oldLevelModifyButton").click(function(){ 
		if ($("#oldLevelModifyForm").form("validate")) {
			$("#oldLevelModifyForm").form({
			    url:"OldLevel/update/" + $("#oldLevel_levelId_modify").val(),
			    onSubmit: function(){
					if($("#oldLevelEditForm").form("validate"))  {
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
			$("#oldLevelModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});
