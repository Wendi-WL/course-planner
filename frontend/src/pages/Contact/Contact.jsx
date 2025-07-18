import Button from "../../components/ui/Button/Button";
import Footer from "../../components/ui/Footer/Footer";
import "./Contact.css";
import TextField from "@mui/material/TextField";
import { useForm } from "react-hook-form";
import emailjs from "@emailjs/browser";

function Contact() {
  const { register, handleSubmit, formState } = useForm();
  const { errors } = formState;

  const sendEmail = ({ yourName, yourEmail, specSubject, msg }) => {
    const templateParams = {
      from_name: yourName,
      from_email: yourEmail,
      subject: specSubject,
      message: msg,
    };
    console.log(templateParams);

    emailjs
      .send("service_asumvkd", "template_kf8b4zr", templateParams, {
        publicKey: "2s3M43dKJ7I3v2XDT",
      })
      .then(
        (result) => {
          console.log(result.text);
        },
        (error) => {
          console.log(error.text);
        }
      );
  };

  // styles for the form
  const fieldStyle = {
    zIndex: "1",
    input: { background: "rgba(245, 244, 244, 0.80);" },
  };
  const shrinkLabel = { inputLabel: { shrink: true } };

  return (
    <div className='contact-page'>
      <div className='title-desc'>
        <h1 className='contact-title'>Contact Us</h1>
        <p className='desc'>
          We'd love to answer any questions and hear any feedback you may have.
        </p>
      </div>
      <section className='main-contact'>
        <form onSubmit={handleSubmit(sendEmail)}>
          <div className='form-container'>
            <TextField
              fullWidth
              name='yourName'
              label='Your Name'
              variant='outlined'
              placeholder='Enter your name'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              {...register("yourName")}
            />
            <TextField
              fullWidth
              required
              name='email'
              label='Your email'
              variant='outlined'
              placeholder='Enter your email'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              type='email'
              {...register("yourEmail", {
                required: "Email is required",
              })}
              error={!!errors.email}
              helperText={errors.email?.message}
            />
            <TextField
              fullWidth
              name='subject'
              label='Subject'
              variant='outlined'
              placeholder='Enter topic of message'
              size='small'
              slotProps={shrinkLabel}
              sx={fieldStyle}
              {...register("specSubject")}
            />
            <TextField
              className='msg-input'
              required
              fullWidth
              name='message'
              label='Message'
              multiline // textarea element rendered instead of input
              rows={5}
              placeholder='Type your questions/feedback here'
              slotProps={shrinkLabel}
              {...register("msg", {
                required: "Message is required",
              })}
              error={!!errors.message}
              helperText={errors.message?.message}
              // sx={fieldStyle}
            />
            <Button
              type='submit'
              text='Send'
            />
          </div>
        </form>
      </section>
      <Footer />
    </div>
  );
}
export default Contact;
