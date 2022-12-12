<template>
    <div id="topNav" >
        <div id="icon">
            <img src="../../assets/logo_big.png" style="margin:auto"/>
        </div>
        <div id="text">
            <p>TEXTMOOD</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'topNav',
}
</script>

<style>
#topNav{
    width:100%;
    height:100%;
}
#icon {
    float:left;
    width:4%;
    height:100%;
}
#text {
    float:left;
    width:96%;
    height:100%;
    text-align: left;
    font-family:Arial,Helvetica,sans-serif;
    color:rgb(10, 11, 11);
}
</style>