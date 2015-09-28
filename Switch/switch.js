$('.BSswitch').bootstrapSwitch('state', true);


$('#CheckBoxValue').text($("#TheCheckBox").bootstrapSwitch('state'));

$('#TheCheckBox').on('switchChange.bootstrapSwitch', function () {

    $("#CheckBoxValue").text($('#TheCheckBox').bootstrapSwitch('state'));
});

$('.probeProbe').bootstrapSwitch('state', true);

$('.probeProbe').on('switchChange.bootstrapSwitch', function (event, state) {

    alert(this);
    alert(event);
    alert(state);
});

$('#toggleSwitches ').click(function () {
    $('.BSswitch ').bootstrapSwitch('toggleDisabled');
    if ($('.BSswitch ').attr('disabled')) {
        $(this).text('Enable All Switches ');
    } else {
        $(this).text('Disable All Switches ');
    }
});