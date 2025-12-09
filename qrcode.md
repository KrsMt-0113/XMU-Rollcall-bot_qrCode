# 二维码逆向笔记

### step 1

注意到二维码内容都是 `/j?p=` 开头，搜索 js 源码获得以下代码片段：

```javascript
var h = e => "".concat(l.location.protocol, "//").concat(l.location.host, "/course/join/").concat(e)
    , g = e => encodeURI("".concat(t.h5Host, "/j?p=").concat(a({
        courseId: p,
        accessCode: e
    })));
    e.$watch("invitingCourseUsers", (function(e) {
        if (e && "" === t.access_code) {
            return r.get("/api/course/".concat(p, "/access_code")).success((function(e) {
                return t.ui.resetable = e.resetable,
                e.access_code ? m(e) : e.resetable ? t.resetAccessCodeAndUrl() : void 0
            }
        )).error((function() {}))
        }
    }
```

可以看到 `/j?p=` 后面的内容是这个 `a({ courseId: p, accessCode: e })` 的结果。

在该段代码上方可以看到 `a` 函数的来源：

```javascript
var a = r(601520).encodeData
```

### step 2

在 `601520` 模块找到 `encodeData` 函数：

```javascript
n.d(t, {
    decodeData: () => sa,
    encodeData: () => aa
});
```

继续在该模块中找到 `aa` 函数：

```javascript
aa = function(e) {
        var t = "";
        return e && "[object Object]" === Object.prototype.toString.call(e) && Object.keys(e).length ? (Object.entries(e).forEach((function(e) {
                var n, r;
                t += (na[n = e[0]] || n) + "~" + ("string" == typeof (r = e[1]) ? ra[r] || r.replaceAll("~", Zo).replaceAll("!", Yo) : "boolean" == typeof r ? r ? ea : ta : "number" == typeof r ? r % 1 == 0 ? Qo + r.toString(36) : Qo + r.toString().split(".").map((function(e) {
                        return Number(e).toString(36)
                    }
                )).join(".") : "NOTSUPPORTED") + "!"
            }
        )),
            t.substring(0, t.length - 1)) : t
    }
```

`na` 和 `ra` 分别是两个映射表：

```javascript
na = Object.fromEntries([
    "courseId",
    "activityId",
    "activityType",
    "data",
    "rollcallId",
    "groupSetId",
    "accessCode",
    "action",
    "enableGroupRollcall",
    "createUser",
    "joinCourse"
].map((function(e, t) {
    return [e, t.toString(36)]
})))
    
ra = Object.fromEntries([
    "classroom-exam",
    "feedback",
    "vote"
].map((function(e, t) {
    return [e, Jo + Number(t + 2).toString(36)]
})))
```

### step 3 (todo)

获得教师端获得 `data` 的方法。在教师端 js 代码中搜索关键词 `/j?p=` 并找到包含 `data` 字段的代码即可。

二维码签到的链接包含三项：courseId、activityId 和 data。

获得 `data` 后的签到实现方法：

- 使用 `PUT` 方法发送签到请求

- 按照 js 逻辑生成链接并 `GET`

然后检查 `response.status_code == 200` 即可。