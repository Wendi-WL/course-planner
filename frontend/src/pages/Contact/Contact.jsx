import Button from "../../components/ui/Button/Button";
import Footer from "../../components/ui/Footer/Footer";
import "./Contact.css";
import TextField from "@mui/material/TextField";

function Contact() {
  // const theme = useTheme();
  // const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <div className='contact-page'>
      <div className='title-desc'>
        <h1 className='contact-title'>Contact Us</h1>
        <p className='desc'>
          We'd love to answer any questions and hear any feedback you may have.
        </p>
      </div>
      <section className='main-contact'>
        <div className='form-container'>
          <TextField
            fullWidth
            label='Your Name'
            variant='outlined'
            placeholder='Enter your name'
            size='small'
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
          <TextField
            required
            fullWidth
            label='Your email'
            variant='outlined'
            placeholder='Enter your email'
            size='small'
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
          <TextField
            required
            fullWidth
            label='Subject'
            variant='outlined'
            placeholder='Enter topic of message'
            size='small'
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
          <TextField
            required
            fullWidth
            label='Message'
            multiline
            rows={4}
            placeholder='Type your questions/feedback here'
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
          <Button text='Send' />
        </div>
      </section>
      <Footer />
    </div>
  );
}
export default Contact;
