import Button from '@mui/material/Button';

const GenericButton = ({ name, onClick }) => {
  return (
    <Button
    type="button"
    variant="contained"
    color="primary"
    onClick={onClick}
    >
    {name}
    </Button>
  )
};

export default GenericButton;
