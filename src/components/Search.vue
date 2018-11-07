<template lang="html">
    <div class="search">
        <form role="search" id="searchform" class="form-search" method="get" action="{% url 'haystack_search' %}">
            <div class="search-group">
                <input id="s" class="search-input" name="q" placeholder=" 搜索..." type="search" required>
            </div>
            <div class="search-group2">
                <button class="search-groups" type="submit" name="submit">搜索</button>
            </div>
        </form>
    </div>
</template>

<script type="text/javascript">
    export default{
        name:"",
        data(){
            return{

            }
        }
    }
</script>

<style type="text/css">
    .search {
        height: 38px;
        background-color: #3D4450;
        padding-top: 5px;
        padding-left: 1%;
        margin-bottom: 40px;
    }
    .search-group {
        float: left;
        width: 85%;
    }
    .search-group2 {
        width: 15%;
        float: left;
    }
    .search-input {
        height: 32px;
        width: 100%;
        font-size: 15px;
    }
    .search-groups {
        float: left;
        text-align: center;
        padding: 7px 10%;
        margin-left: 20%;
        background-color: #D9534F;
        color: #FFFFFF;
        border: 0px;
    }
</style>