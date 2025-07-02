import "./Contact.css";
import TextField from "@mui/material/TextField";

function Contact() {
  // const theme = useTheme();
  // const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <div className='Page'>
      <div className='title-desc'>
        <h1>Contact Us</h1>
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
            size='medium'
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
            size='medium'
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
            placeholder='What is the message about?'
            size='medium'
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
          />
          <TextField
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
        </div>
      </section>
    </div>
  );
}
export default Contact;
