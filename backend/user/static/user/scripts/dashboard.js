function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

function setDetectBtn(op_id) {
    $("#detect_btn").click(function () {
        $("#status").text("正在进行图片转换，请稍候……")
        $("#function_block").hide()
        $.ajax({
            type: "POST",
            url: "../operation/0/net/",
            data: {"id": op_id},
            success: function (res) {
                console.log("emotion", res.emotion)
                console.log("cropped", res.cropped)
                $("#emotion").attr("src", "../" + res.emotion)
                if (res.cropped.length > 0) {
                    $("#crop").attr("src", "../" + res.cropped)
                }
                $("#status").text("已完成转换，刷新页面可以查看操作记录")
            }
        })
    })
}

function setGenderBtn(op_id) {
    $("#gender_btn").click(function () {
        $("#status").text("正在进行图片转换，请稍候……")
        $("#function_block").hide()
        $.ajax({
            type: "POST",
            url: "../operation/1/net/",
            data: {"id": op_id},

            success: function (res) {
                console.log(res.gender)
                console.log(res.cropped)
                $("#gender").attr("src", "../" + res.gender)
                if (res.cropped.length > 0) {
                    $("#crop").attr("src", "../" + res.cropped)
                }
                $("#status").text("已完成转换，刷新页面可以查看操作记录")
            }
        })
    })
}

function setAllBtn(op_id) {
    $("#all_btn").click(function () {
        $("#status").text("正在进行图片转换，请稍候……")
        $("#function_block").hide()
        $.ajax({
            type: "POST",
            url: "../operation/0/net/",
            data: {"id": op_id},
            success: function (res) {
                console.log(res)
                console.log(res.emotion)
                console.log(res.cropped)
                $("#emotion").attr("src", "../" + res.emotion)
                if (res.cropped.length > 0) {
                    $("#crop").attr("src", "../" + res.cropped)
                }
                $("#status").text("已完成转换，刷新页面可以查看操作记录")
            }
        })
        $.ajax({
            type: "POST",
            url: "../operation/1/net/",
            data: {"id": op_id},
            success: function (res) {
                console.log(res.gender)
                console.log(res.cropped)
                $("#gender").attr("src", "../" + res.gender)
                if (res.cropped.length > 0) {
                    $("#crop").attr("src", "../" + res.cropped)
                }
                $("#status").text("已完成转换，刷新页面可以查看操作记录")
            }
        })
    })
}

$(document).ready(function () {
    let explore_btn = $("#explore_btn")
    let upload_btn = $("#upload_btn")
    let file_input = $("#file_input")
    let file_addr = $("#file_addr")
    let web_addr = $("#web_addr")
    let logout_btn = $("#logoutBtn")
    let delete_btns = $(".delete-btn")
    let delete_all_btn = $("#delete-all-btn")

    $("#function_block").hide()

    explore_btn.click(function () {
        file_input.click()
    })

    file_input.change(function () {
        file_addr.val(file_input.val())
        let formData = new FormData();
        formData.append("image", file_input[0].files[0]);
        $.ajax({
            url: "../operation/upload/",
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                console.log(res)
                if (res.addr) {
                    $("#preview").attr("src", "../static/" + res.addr)
                    upload_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    explore_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    $("#file_desc").text("本地图片已经上传")
                    $("#web_desc").text("已禁用网络上传")
                    $("#status").text("图片已经上传，请选择您的服务")
                    $("#function_block").show()
                    setDetectBtn(res.id)
                    setGenderBtn(res.id)
                    setAllBtn(res.id)
                }
                else if (res.error) {
                    $("#file_desc").text("本地图片上传失败，请重新选择")
                }
            }
        })
    })

    upload_btn.click(function () {
        let file_web = web_addr.val()
        console.log(file_web)
        $.post(
            "../operation/upload/",
            {"url": file_web},
            function (res) {
                console.log(res)
                if (res.addr) {
                    $("#preview").attr("src", "../static/" + res.addr)
                    upload_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    explore_btn.attr("disabled", true)
                    file_addr.attr("disabled", true)
                    $("#file_desc").text("已禁用本地上传")
                    $("#web_desc").text("网络图片已上传")
                    $("#status").text("图片已经上传，请选择您的服务")
                    $("#function_block").show()
                    setDetectBtn(res.id)
                    setGenderBtn(res.id)
                    setAllBtn(res.id)
                }
                else if (res.error) {
                    $("#web_desc").text("网络图片上传失败，请换一张")
                }
            }
        )
    })

    logout_btn.click(function () {
        window.location.replace("../logout/")
    })

    delete_btns.each(function () {
        this.onclick = function () {
            console.log(this)
            let operation_id = this.id
            $.post(
                "../operation/delete/",
                {"ids": [operation_id]},
                function (res) {
                    window.location.replace("../dashboard/")
                }
            )
        }
    })

    delete_all_btn.click(function () {
        let ids = []
        let checkboxes = $(".checkbox")
        checkboxes.each(function () {
            if (this.checked && this.id !== "checkall") {
                ids.push(this.id.substring(11))
            }
        })
        $.post(
            "../operation/delete/",
            {"ids": ids},
            function (res) {
                window.location.replace("../dashboard/")
            }
        )
    })

    $("#checkall").click(function () {
        $(".checkbox").prop("checked", this.checked)
    })

    $("#query-btn").click(function () {
        date1 = $("#date1").val()
        date2 = $("#date2").val()
        console.log(date1, date2)
        if (date1.length > 0 && date2.length > 0) {
            href_path = "../dashboard/?range=yes"
            href_time1 = "&start=" + date1
            href_time2 = "&end=" + date2
            window.location.replace(href_path + href_time1 + href_time2)
        }
    })

    if (GetQueryString("range") === "yes") {
        $("#timequery").addClass("active")
        $("#allrecord").removeClass("active")
    }

})