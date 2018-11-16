<template lang="html">
        <div class="body-left">
            <div v-if="!blogshow" class="blog" v-for="blog in blogs">
                <div class="blog-head">
                    <h1>
                        <a @click="ShowDetail(blog.id)" href="#">{{ blog.title }}</a>
                    </h1>
                </div>
                <div class="blog-info">
                    <span class="span-info"><a href="#">&nbsp;{{ blog.category }}&nbsp;</a></span>
                    <span class="span-info"><a href="#">&nbsp;{{ blog.author }}&nbsp;</a></span>
                    <span class="span-info">&nbsp;{{ blog.create_time }}&nbsp;</span>
                    <span class="span-info">&nbsp;{{ blog.views }} 阅读&nbsp;</span>
                </div>
                <div class="blog-execrpt"><span>{{ blog.digested }}     </span></div>
                <div class="blog-link"><span><a @click="ShowDetail(blog.id)" >阅读全文</a></span></div>
            </div>
            <div v-if="blogshow" class="blog">
                <div class="blog-head">
                    <h1>
                        <a >{{ blogdetail.title }}</a>
                    </h1>
                </div>
                <div class="blog-info">
                    <span class="span-info"><a href="#">&nbsp;{{ blogdetail.category }}&nbsp;</a></span>
                    <span class="span-info"><a href="#">&nbsp;{{ blogdetail.author }}&nbsp;</a></span>
                    <span class="span-info">&nbsp;{{ blogdetail.create_time }}&nbsp;</span>
                    <span class="span-info">&nbsp;{{ blogdetail.views }} 阅读&nbsp;</span>
                </div>
                <div class="entry-content" v-html="blogdetail.body"><span class=""></span></div>
            </div>
        </div>
</template>

<script type="text/javascript">
    export default{
        name:"list",
        data(){
            return{
                blogs:[],
                blogshow:false,
                blogdetail:[],
            }
        },
        props:{
            CategoryId:String,
        },
        mounted(){
            var _this = this
            this.bus.$on('blogdetail', function(val1,val2){
                _this.blogshow = val1;
                _this.blogdetail = val2;
            })
            this.bus.$on('taglist', function(val1, val2){
                _this.blogshow = val1;
                _this.blogs = val2;
            })
        },
        methods:{
            GetBlog(){
                //var url = "/static/Category" + this.CategoryId + ".json";
                //this.$axios.get(url)
                var url = this.HOST + "category";
                this.$axios.get(url, {
                    params:{
                        flag: this.CategoryId
                    }
                })
                .then(res => {
                    this.blogshow = false;
                    this.blogs =  res.data.data;
                    this.bus.$emit('toc', '', false);
                })
                .catch(error => {
                    console.log(error);
                })
            },
            ShowDetail(Id){
                var url = this.HOST + "detail";
                console.log(url+Id);
                this.$axios.get(url, {
                    params:{
                        id:Id
                    }
                })
                .then(res => {
                    if (res.data.status == 0){
                        this.blogshow = true;
                        var blog = res.data.data;
                        var result = blog.body.match(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/);
                        if (result != null){
<<<<<<< HEAD
                            result = result[0]
=======
                            result = result[0];
                            this.bus.$emit('toc', result,true);
                        } else{
                            this.bus.$emit('toc', '', false);
>>>>>>> 8aca13b5a498a108c0c63dc124cebbfe541abb0c
                        }
                        blog.body = blog.body.replace(/(<div class="toc">(?:.|\n)*<\/ul>\n<\/div>)/, "");
                        this.blogdetail = blog;
                        this.bus.$emit('add', false);
                    }
                })
                .catch(error => {
                    console.log(error);
                })
            }
        },
        watch:{
            CategoryId(val){
                this.CategoryId = val;
                this.GetBlog();
            }
        },
        created(){
            this.GetBlog();
        }
    }
</script>

<style type="text/css">
    .body-left{
        float: left;
        width: 65%;
    }
    .blog {
        background-color: #d8d4d473 !important;
        width: 100%;
        margin-bottom: 35px;
    }
    .blog-head {
        padding-top: 20px;
        padding-bottom: 10px;
    }
    .blog-head h1 {
        text-align: center;
    }
    .blog-head h1 a{
        text-decoration:none;
        color: #0b445b;
    }
    .blog-info {
        text-align: center;
        padding-top: 10px;
        padding-bottom:20px;
    }
    .blog-info span{
        background-color: #3D4450;
        color: #FFFFFF;
    }
    .blog-info span a{
        text-decoration:none;
        color: #FFFFFF;
    }
    .blog-execrpt {
        margin:0 30px;
        padding: 10px 20px;
        height: auto;
        background-color: #EEEEEE;
        font-size: 14px;
        line-height: 1.428571429;
    }
    .blog-execrpt span{

    }
    .blog-link {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .blog-link a{
        text-decoration:none;
    }
    .entry-content {
        font-size: 14px;
        line-height: 1.5;
        font-weight: 300;
        padding-left: 20px;
        color: #000;

        word-wrap:break-word;
        word-break:break-all;
        overflow: hidden;

    }
    .entry-content a{
        text-decoration:none;
    }


/* CODE
=============================================================================*/

pre, code, tt {
  font-size: 12px;
  font-family: Consolas, "Liberation Mono", Courier, monospace;
}

code, tt {
  margin: 0 0px;
  padding: 0px 0px;
  white-space: nowrap;
  border: 1px solid #eaeaea;
  background-color: #f8f8f8;
  border-radius: 3px;
}

pre>code {
  margin: 0;
  padding: 0;
  white-space: pre;
  border: none;
  background: transparent;
}

pre {
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  font-size: 13px;
  line-height: 19px;
  overflow: auto;
  padding: 6px 0;
  padding-left: 28px;
  border-radius: 3px;
}

pre code, pre tt {
  background-color: transparent;
  border: none;
}

kbd {
    -moz-border-bottom-colors: none;
    -moz-border-left-colors: none;
    -moz-border-right-colors: none;
    -moz-border-top-colors: none;
    background-color: #DDDDDD;
    background-image: linear-gradient(#F1F1F1, #DDDDDD);
    background-repeat: repeat-x;
    border-color: #DDDDDD #CCCCCC #CCCCCC #DDDDDD;
    border-image: none;
    border-radius: 2px 2px 2px 2px;
    border-style: solid;
    border-width: 1px;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    line-height: 10px;
    padding: 1px 4px;
}

/* QUOTES
=============================================================================*/

blockquote {
  border-left: 4px solid #DDD;
  padding: 0 10px;
  color: #777;
}

blockquote>:first-child {
  margin-top: 0px;
}

blockquote>:last-child {
  margin-bottom: 0px;
}

.codehilite .hll { background-color: #ffffcc }
.codehilite  { background: #f8f8f8; }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #808080 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0040D0 } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
</style>